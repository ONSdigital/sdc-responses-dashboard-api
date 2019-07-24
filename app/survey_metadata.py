from structlog import get_logger

from app.controllers.collection_exercise_controller import get_collection_exercise_list
from app.controllers.survey_controller import get_survey_list
from app.exceptions import UnknownSurveyError

import pprint

logger = get_logger()


def map_surveys_to_collection_exercises(surveys, collection_exercises) -> list:
    survey_data = {
        survey['id']: {
            'surveyId': survey['id'],
            'shortName': survey['shortName'],
            'longName': survey['longName'],
            'surveyRef': survey['surveyRef'],
            'surveyType': survey['surveyType'],
            'collectionExercises': []
        } for survey in surveys if survey['id'] in [ex['surveyId'] for ex in collection_exercises]
    }

    for collection_exercise in collection_exercises:
        try:
            survey_data[collection_exercise['surveyId']]['collectionExercises'].append(
                {
                    'collectionExerciseId': collection_exercise['id'],
                    'userDescription': collection_exercise['userDescription'],
                    'exerciseRef': collection_exercise['exerciseRef'],
                    'scheduledExecutionDateTime': collection_exercise['scheduledExecutionDateTime'],
                    'scheduledReturnDateTime': collection_exercise['scheduledReturnDateTime']
                }
            )
        except KeyError as e:
            if str(e) == f"'{collection_exercise['surveyId']}'":
                message = 'Reference to unknown survey id in collection exercise'
                logger.error(message, collection_exercise_id=collection_exercise['id'])
                raise UnknownSurveyError(
                    message=message, survey_id=['surveyId'])
            raise

    return list(survey_data.values())


def map_collection_exercise_id_to_survey_id(surveys_to_collection_exercises) -> dict:
    collection_exercises_to_survey_ids = {}
    for survey in surveys_to_collection_exercises:
        for collection_exercise in survey['collectionExercises']:
            collection_exercises_to_survey_ids[collection_exercise['collectionExerciseId']] = {
                'surveyId': survey['surveyId'],
                'shortName': survey['shortName'],
                'longName': survey['longName'],
                'surveyType': survey['surveyType'],
                'userDescription': collection_exercise['userDescription'],
                'scheduledExecutionDateTime': collection_exercise['scheduledExecutionDateTime'],
                'scheduledReturnDateTime': collection_exercise['scheduledReturnDateTime'],
                'exerciseRef': collection_exercise['exerciseRef']
            }

    return collection_exercises_to_survey_ids


def fetch_survey_and_collection_exercise_metadata() -> (list, dict):
    collection_exercises = get_collection_exercise_list()
    live_collection_exercises = _filter_ready_collection_exercises(collection_exercises)
    surveys = get_survey_list()

    surveys_to_collection_exercises = _filter_surveys_to_business_surveys(
        map_surveys_to_collection_exercises(
            surveys,
            live_collection_exercises))

    collection_exercises_to_survey_ids = _filter_collection_exercise_to_business_surveys(
        map_collection_exercise_id_to_survey_id(
            surveys_to_collection_exercises))

    return surveys_to_collection_exercises, collection_exercises_to_survey_ids


def _filter_ready_collection_exercises(collection_exercises: list) -> list:
    return [
        collection_exercise
        for collection_exercise in collection_exercises
        if collection_exercise['state'] in {'READY_FOR_LIVE', 'LIVE'}
    ]


def _filter_surveys_to_business_surveys(surveys: list) -> list:
    return [
        survey for survey in surveys
        if survey['surveyType'] == 'Business'
    ]


def _filter_collection_exercise_to_business_surveys(collection_exercises: dict) -> dict:
    return {
        k: v for k, v in collection_exercises.items() if v['surveyType'] == 'Business'
    }
