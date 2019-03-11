import json
import os

import responses
from requests import HTTPError

from app.controllers.collection_exercise_controller import get_collection_exercise_event_date
from app.controllers.collection_exercise_controller import get_collection_exercise_list
from tests.app import AppContextTestCase


class TestCollectionExerciseController(AppContextTestCase):
    current_file_path = os.path.dirname(__file__)

    @responses.activate
    def test_get_collection_exercise_list_success(self):
        collection_exercises_response = self.get_collection_exercises_response()

        with self.app.app_context():
            responses.add(responses.GET, f'{self.app.config["COLLECTION_EXERCISE_URL"]}/collectionexercises',
                          json=collection_exercises_response, status=200)

            controller_output = get_collection_exercise_list()

        self.assertEqual(collection_exercises_response, controller_output)

    @responses.activate
    def test_get_collection_exercise_list_auth_failure_raises_http_error(self):
        with self.app.app_context():
            responses.add(responses.GET, f'{self.app.config["COLLECTION_EXERCISE_URL"]}/collectionexercises',
                          status=401)

            with self.assertRaises(HTTPError):
                get_collection_exercise_list()

    @responses.activate
    def test_get_collection_exercise_event_date_success(self):
        collection_exercise_go_live_response = self.get_collection_exercise_go_live_response()
        collection_exercise_id = collection_exercise_go_live_response['collectionExercise']['id']
        with self.app.app_context():
            responses.add(responses.GET, f'{self.app.config["COLLECTION_EXERCISE_URL"]}'
            f'/collectionexercises/{collection_exercise_id}/events/go_live', json=collection_exercise_go_live_response,
                          status=200)

            controller_output = get_collection_exercise_event_date(self.app.config['COLLECTION_EXERCISE_URL'],
                                                                   self.app.config['AUTH_USERNAME'],
                                                                   self.app.config['AUTH_PASSWORD'],
                                                                   collection_exercise_id=collection_exercise_id,
                                                                   event_tag='go_live')

        self.assertEqual(collection_exercise_go_live_response['timestamp'], controller_output)

    @responses.activate
    def test_get_collection_exercise_event_date_returns_none_on_error_status_code(self):
        collection_exercise_go_live_response = self.get_collection_exercise_go_live_response()
        collection_exercise_id = collection_exercise_go_live_response['collectionExercise']['id']
        with self.app.app_context():
            responses.add(responses.GET, f'{self.app.config["COLLECTION_EXERCISE_URL"]}'
            f'/collectionexercises/{collection_exercise_id}/events/go_live', status=500)

            controller_output = get_collection_exercise_event_date(self.app.config['COLLECTION_EXERCISE_URL'],
                                                                   self.app.config['AUTH_USERNAME'],
                                                                   self.app.config['AUTH_PASSWORD'],
                                                                   collection_exercise_id=collection_exercise_id,
                                                                   event_tag='go_live')

        self.assertEqual(None, controller_output)

    @responses.activate
    def test_get_collection_exercise_event_date_returns_none_missing_timestamp(self):
        collex_go_live_missing_timestamp_response = self.get_collection_exercise_go_live_missing_timestamp_response()
        collection_exercise_id = collex_go_live_missing_timestamp_response['collectionExercise']['id']

        with self.app.app_context():
            responses.add(responses.GET, f'{self.app.config["COLLECTION_EXERCISE_URL"]}'
            f'/collectionexercises/{collection_exercise_id}/events/go_live',
                          json=collex_go_live_missing_timestamp_response, status=200)

            controller_output = get_collection_exercise_event_date(self.app.config['COLLECTION_EXERCISE_URL'],
                                                                   self.app.config['AUTH_USERNAME'],
                                                                   self.app.config['AUTH_PASSWORD'],
                                                                   collection_exercise_id=collection_exercise_id,
                                                                   event_tag='go_live')

        self.assertEqual(None, controller_output)

    def get_collection_exercises_response(self):
        with open(os.path.join(self.current_file_path,
                               '../../test_data'
                               '/get_collection_exercises_response.json')) as fp:
            collection_exercises_response = json.load(fp)
        return collection_exercises_response

    def get_collection_exercise_go_live_response(self):
        with open(os.path.join(self.current_file_path,
                               '../../test_data'
                               '/get_collection_exercise_go_live_response.json')) as fp:
            collection_exercise_go_live_response = json.load(fp)
        return collection_exercise_go_live_response

    def get_collection_exercise_go_live_missing_timestamp_response(self):
        with open(os.path.join(self.current_file_path,
                               '../../test_data'
                               '/get_collection_exercise_go_live_missing_timestamp_response.json')) as fp:
            collection_exercise_go_live_missing_timestamp_response = json.load(fp)
        return collection_exercise_go_live_missing_timestamp_response
