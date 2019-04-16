import json

from flask import Blueprint, abort, request
from structlog import get_logger

from app.collection_exercise_event_dates import get_collection_exercises_event_dates
from app.validators import parse_uuid

collection_exercise_dates_blueprint = Blueprint(name='collection_exercise_events',
                                                import_name=__name__,
                                                url_prefix='/dashboard')

logger = get_logger()


@collection_exercise_dates_blueprint.route('/collection-exercises/event/<event_tag>', methods=['GET'])
def collection_exercises_event_dates(event_tag):
    collection_exercises = request.args.getlist('collexIDs[]')
    if not collection_exercises:
        abort(400, 'No collection exercise IDs received')

    for collection_exercise_id in collection_exercises:
        parsed_collection_exercise_id = parse_uuid(collection_exercise_id)
        if not parsed_collection_exercise_id:
            logger.debug('Received malformed collection exercise ID',
                         invalid_collection_exercise_id=collection_exercise_id)
            abort(400, f'Malformed collection exercise ID: {collection_exercise_id}')

    event_dates = get_collection_exercises_event_dates(collection_exercises, event_tag)

    return json.dumps(event_dates)
