import logging
import os
import sys

from flask import Flask, url_for, current_app
from flask_cors import CORS
import structlog
from structlog import wrap_logger
from structlog.processors import JSONRenderer
from structlog.processors import TimeStamper, format_exc_info
from structlog.stdlib import add_log_level, add_logger_name, filter_by_level, LoggerFactory
from structlog.threadlocal import wrap_dict

from app.errors.handlers import api_connection_error
from app.exceptions import MissingConfigError, APIConnectionError
import config


def create_app():

    app_config = getattr(config, os.getenv('APP_SETTINGS', 'Config'))
    check_required_config(app_config)

    app = Flask(__name__, static_url_path='/dashboard/static')
    app.url_map.strict_slashes = False

    CORS(app)

    app.config.from_object(app_config)

    _configure_logger(app.config['LOGGING_LEVEL'])
    logger = wrap_logger(logging.getLogger(__name__))
    logger.info('Logger created', log_level=app.config['LOGGING_LEVEL'])
    logger.debug('App configuration set', config=app_config)

    add_blueprints(app)
    add_error_handlers(app)

    @app.context_processor
    def override_url_for():  # pylint: disable=unused-variable
        return dict(url_for=versioned_url_for)

    return app


def add_blueprints(app):

    from app.api.health import health_blueprint
    from app.views.dashboard import dashboard_blueprint
    from app.api.reporting import reporting_blueprint
    from app.api.collection_exercise_dates import collection_exercise_dates_blueprint

    app.register_blueprint(health_blueprint)
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(reporting_blueprint)
    app.register_blueprint(collection_exercise_dates_blueprint)


def add_error_handlers(app):

    from app.errors.handlers import not_found_error, internal_server_error

    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(APIConnectionError, api_connection_error)


def versioned_url_for(endpoint, **values):

    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            values['filename'] = filename
            values['q'] = current_app.config['STATIC_ASSETS_VERSION']

    return url_for(endpoint, **values)


def _configure_logger(level='INFO', indent=None):
    logging.basicConfig(stream=sys.stdout, level=level, format='%(message)s')

    try:
        indent = int(os.getenv('LOGGING_JSON_INDENT') or indent)
    except TypeError:
        indent = None
    except ValueError:
        indent = None

    def add_service(_, __, event_dict):
        """
        Add the service name to the event dict.
        """
        event_dict['service'] = os.getenv('NAME', 'sdc-responses-dashboard')
        return event_dict

    renderer_processor = JSONRenderer(indent=indent)
    processors = [add_log_level, filter_by_level, add_service, format_exc_info, add_logger_name,
                  TimeStamper(fmt='%Y-%m-%dT%H:%M%s', utc=True, key='created_at'), renderer_processor]
    structlog.configure(context_class=wrap_dict(dict), logger_factory=LoggerFactory(), processors=processors,
                        cache_logger_on_first_use=True)


def check_required_config(app_config):
    missing_vars = {var for var in config.REQUIRED_ENVIRONMENT_VARIABLES if not vars(app_config).get(var)}
    if missing_vars:
        raise MissingConfigError(missing_vars)
