import json
import os
from time import sleep
from unittest.mock import patch

import responses

from app.collection_exercise_event_dates import get_collection_exercises_event_dates
from tests.app import AppContextTestCase


def mock_get_collection_exercise_event_date(*args):
    if args[3] == 'collex-id-raise-exception':
        raise Exception
    elif args[3] == 'collex-id-timeout':
        sleep(30)
    else:
        return '2018-12-14T00:00:00.000Z'


class TestCollectionExerciseEventDates(AppContextTestCase):
    current_file_path = os.path.dirname(__file__)

    def get_first_collection_exercise_go_live_response(self):
        with open(os.path.join(self.current_file_path,
                               '../test_data/get_collection_exercise_go_live_response.json')) as fp:
            collection_exercise_go_live_response = json.load(fp)
        return collection_exercise_go_live_response

    def get_second_collection_exercise_go_live_response(self):
        with open(os.path.join(self.current_file_path,
                               '../test_data/get_collection_exercise_go_live_second_response.json')) as fp:
            collection_exercise_go_live_response = json.load(fp)
        return collection_exercise_go_live_response

    def get_collection_exercise_go_live_missing_timestamp_response(self):
        with open(os.path.join(self.current_file_path,
                               '../test_data/get_collection_exercise_go_live_missing_timestamp_response.json')) as fp:
            collection_exercise_go_live_response = json.load(fp)
        return collection_exercise_go_live_response

    @responses.activate
    def test_get_two_collection_exercises_event_dates_success(self):
        first_collection_exercise_go_live_response = self.get_first_collection_exercise_go_live_response()
        first_collection_exercise_id = first_collection_exercise_go_live_response['collectionExercise']['id']

        second_collection_exercise_go_live_response = self.get_second_collection_exercise_go_live_response()
        second_collection_exercise_id = second_collection_exercise_go_live_response['collectionExercise']['id']

        with self.app.app_context():
            responses.add(
                responses.GET,
                (f'{self.app.config["COLLECTION_EXERCISE_URL"]}'
                 f'/collectionexercises/{first_collection_exercise_id}/events/go_live'),
                json=first_collection_exercise_go_live_response,
                status=200)
            responses.add(
                responses.GET,
                (f'{self.app.config["COLLECTION_EXERCISE_URL"]}'
                 f'/collectionexercises/{second_collection_exercise_id}/events/go_live'),
                json=second_collection_exercise_go_live_response,
                status=200)
            actual_timestamps = get_collection_exercises_event_dates(
                [first_collection_exercise_id, second_collection_exercise_id],
                event_tag='go_live')

        self.assertEqual({
            first_collection_exercise_id: first_collection_exercise_go_live_response['timestamp'],
            second_collection_exercise_id: second_collection_exercise_go_live_response['timestamp']
        },
            actual_timestamps)

    @responses.activate
    def test_get_two_collection_exercises_event_dates_with_one_missing_timestamp(self):
        first_collection_exercise_go_live_response = self.get_first_collection_exercise_go_live_response()
        first_collection_exercise_id = first_collection_exercise_go_live_response['collectionExercise']['id']

        go_live_missing_timestamp_response = self.get_collection_exercise_go_live_missing_timestamp_response()
        collection_exercise_id_missing_timestamp = go_live_missing_timestamp_response['collectionExercise']['id']

        with self.app.app_context():
            responses.add(
                responses.GET,
                (f'{self.app.config["COLLECTION_EXERCISE_URL"]}'
                 f'/collectionexercises/{first_collection_exercise_id}/events/go_live'),
                json=first_collection_exercise_go_live_response,
                status=200)
            responses.add(
                responses.GET,
                (f'{self.app.config["COLLECTION_EXERCISE_URL"]}'
                 f'/collectionexercises/{collection_exercise_id_missing_timestamp}/events/go_live'),
                json=go_live_missing_timestamp_response,
                status=200)
            actual_timestamps = get_collection_exercises_event_dates(
                [first_collection_exercise_id, collection_exercise_id_missing_timestamp],
                event_tag='go_live')

        self.assertEqual({
            first_collection_exercise_id: first_collection_exercise_go_live_response['timestamp'],
            collection_exercise_id_missing_timestamp: None
        },
            actual_timestamps)

    @responses.activate
    def test_get_two_collection_exercises_event_dates_with_one_error_response(self):
        first_collection_exercise_go_live_response = self.get_first_collection_exercise_go_live_response()
        first_collection_exercise_id = first_collection_exercise_go_live_response['collectionExercise']['id']

        second_collection_exercise_go_live_response = self.get_second_collection_exercise_go_live_response()
        second_collection_exercise_id = second_collection_exercise_go_live_response['collectionExercise']['id']

        with self.app.app_context():
            responses.add(
                responses.GET,
                (f'{self.app.config["COLLECTION_EXERCISE_URL"]}'
                 f'/collectionexercises/{first_collection_exercise_id}/events/go_live'),
                json=first_collection_exercise_go_live_response,
                status=200)
            responses.add(
                responses.GET,
                (f'{self.app.config["COLLECTION_EXERCISE_URL"]}'
                 f'/collectionexercises/{second_collection_exercise_id}/events/go_live'),
                status=500)
            actual_timestamps = get_collection_exercises_event_dates(
                [first_collection_exercise_id, second_collection_exercise_id],
                event_tag='go_live')

        self.assertEqual({
            first_collection_exercise_id: first_collection_exercise_go_live_response['timestamp'],
            second_collection_exercise_id: None
        },
            actual_timestamps)

    @patch('app.collection_exercise_event_dates.get_collection_exercise_event_date',
           new=mock_get_collection_exercise_event_date)
    def test_get_two_collection_exercises_event_dates_with_one_exception_in_controller(self):
        first_collection_exercise_id = '00000000-0000-0000-0000-000000000000'
        second_collection_exercise_id = 'collex-id-raise-exception'

        with self.app.app_context():
            actual_timestamps = get_collection_exercises_event_dates(
                [first_collection_exercise_id, second_collection_exercise_id],
                event_tag='go_live')

        self.assertEqual({
            first_collection_exercise_id: '2018-12-14T00:00:00.000Z',
            second_collection_exercise_id: None
        },
            actual_timestamps)
