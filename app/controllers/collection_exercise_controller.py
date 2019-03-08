import requests
from flask import current_app
from structlog import get_logger

from app.exceptions import APIConnectionError

logger = get_logger()


def get_collection_exercise_list():
    url = f'{current_app.config["COLLECTION_EXERCISE_URL"]}/collectionexercises'
    logger.debug('Attempting to retrieve collection exercises')
    try:
        response = requests.get(
            url,
            auth=requests.auth.HTTPBasicAuth(current_app.config['AUTH_USERNAME'],
                                             current_app.config['AUTH_PASSWORD']))
    except requests.exceptions.ConnectionError:
        raise APIConnectionError('Failed to connect to collection exercise service')
    if response.status_code != 200:
        logger.error('Failed to retrieve collection exercises',
                     status_code=response.status_code,
                     response=response.content)
        response.raise_for_status()
    logger.debug('Successfully retrieved collection exercises')
    return response.json()


def get_collection_exercise_event_date(collection_exercise_url: str, username: str, password: str,
                                       collection_exercise_id: str, event_tag: str):
    # The URL, username and password are passed in so that this
    # controller does not have to interact with the app context

    url = f'{collection_exercise_url}/collectionexercises/{collection_exercise_id}/events/{event_tag}'
    logger.debug('Attempting to retrieve event date for collection exercise',
                 collection_exercise_id=collection_exercise_id, event_tag=event_tag)
    try:
        response = requests.get(
            url,
            auth=requests.auth.HTTPBasicAuth(username=username,
                                             password=password))
    except requests.exceptions.HTTPError:
        raise APIConnectionError('Failed to connect to collection exercise service')
    if response.status_code != 200:
        logger.error('Error retrieving event date for collection exercise',
                     collection_exercise_id=collection_exercise_id,
                     event_tag=event_tag,
                     status_code=response.status_code,
                     response=response.content)
        return None
    logger.debug('Successfully retrieved event date for collection exercise',
                 collection_exercise_id=collection_exercise_id, event_tag=event_tag)
    event_timestamp = response.json().get('timestamp')
    return event_timestamp
