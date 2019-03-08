from concurrent.futures import ThreadPoolExecutor, as_completed

from flask import current_app
from structlog import get_logger

from app.controllers.collection_exercise_controller import get_collection_exercise_event_date

logger = get_logger()


def get_collection_exercises_event_dates(collection_exercises: list, event_tag: str):
    event_dates = {}
    with ThreadPoolExecutor(max_workers=len(collection_exercises)) as executor:
        future_to_collection_exercise_id = {
            executor.submit(get_collection_exercise_event_date,
                            current_app.config['COLLECTION_EXERCISE_URL'],
                            current_app.config['AUTH_USERNAME'],
                            current_app.config['AUTH_PASSWORD'],
                            collection_exercise_id,
                            event_tag): collection_exercise_id
            for collection_exercise_id in collection_exercises
        }

        for future in as_completed(future_to_collection_exercise_id):
            collection_exercise_id = future_to_collection_exercise_id[future]
            try:
                event_timestamp = future.result()
            except Exception:  # pylint: disable=broad-except
                logger.error('Error retrieving collection exercise event dates',
                             collection_exercise_id=collection_exercise_id,
                             event_tag=event_tag)
                event_dates[collection_exercise_id] = None
            else:
                event_dates[collection_exercise_id] = event_timestamp

    return event_dates
