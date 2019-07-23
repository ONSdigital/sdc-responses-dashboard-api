from flask import current_app
import requests
from requests.auth import HTTPBasicAuth
import requests.exceptions
from structlog import get_logger

from app.exceptions import APIConnectionError

logger = get_logger()


def get_collection_exercise_list():
    return _get_from_collection_exercise_service('', 'collection exercises')
    

def get_collection_exercise_events(ce_id):
    return _get_from_collection_exercise_service(f'{ce_id}/events', 'collection exercise events')


def _get_from_collection_exercise_service(url, name):
    url = f'{current_app.config["COLLECTION_EXERCISE_URL"]}/collectionexercises/{url}'
    logger.debug(f'Attempting to retrieve {name}')
    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(current_app.config['AUTH_USERNAME'],
                               current_app.config['AUTH_PASSWORD']))
    except requests.exceptions.ConnectionError:
        raise APIConnectionError('Failed to connect to collection exercise service whilst fetching {name}')
    if response.status_code != 200:
        logger.error('Failed to retrieve {name}',
                     status_code=response.status_code,
                     response=response.content)
        response.raise_for_status()
    logger.debug('Successfully retrieved {name}')
    return response.json()
