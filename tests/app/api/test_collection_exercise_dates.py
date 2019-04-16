import json
import os

import responses

from tests.app import AppContextTestCase


class TestCollectionExerciseDates(AppContextTestCase):
    current_file_path = os.path.dirname(__file__)

    @responses.activate
    def test_collection_exercises_event_dates_success(self):
        first_collex_response = self.get_first_collection_exercise_go_live_response()
        first_collex_id = first_collex_response['collectionExercise']['id']
        second_collex_response = self.get_first_collection_exercise_go_live_response()
        second_collex_id = second_collex_response['collectionExercise']['id']

        with self.app.app_context():
            responses.add(responses.GET, (f'{self.app.config["COLLECTION_EXERCISE_URL"]}'
                                          f'/collectionexercises/{first_collex_id}'
                                          f'/events/go_live'), json=first_collex_response, status=200)
            responses.add(responses.GET, (f'{self.app.config["COLLECTION_EXERCISE_URL"]}'
                                          f'/collectionexercises/{second_collex_id}'
                                          f'/events/go_live'), json=second_collex_response, status=200)
            response = self.test_client.get(f'dashboard/collection-exercises/event/go_live'
                                            f'?collexIDs[]={first_collex_id}'
                                            f'&collexIDs[]={second_collex_id}')

        expected_reponse = {first_collex_id: first_collex_response['timestamp'],
                            second_collex_id: second_collex_response['timestamp']}

        self.assertEqual(expected_reponse, json.loads(response.data))

    def test_collection_exercises_event_dates_malformed_id_responds_400(self):
        with self.app.app_context():
            response = self.test_client.get(f'dashboard/collection-exercises/event/go_live'
                                            f'?collexIDs[]=not-a-valid-uuid')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Malformed collection exercise ID: not-a-valid-uuid', response.data)

    def test_collection_exercises_event_dates_no_ids_returns_400(self):
        with self.app.app_context():
            response = self.test_client.get(f'dashboard/collection-exercises/event/go_live')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No collection exercise IDs received', response.data)

    def get_first_collection_exercise_go_live_response(self):
        with open(os.path.join(self.current_file_path,
                               '../../test_data/get_collection_exercise_go_live_response.json')) as fp:
            collection_exercise_go_live_response = json.load(fp)
        return collection_exercise_go_live_response

    def get_second_collection_exercise_go_live_response(self):
        with open(os.path.join(self.current_file_path,
                               '../../test_data/get_collection_exercise_go_live_second_response.json')) as fp:
            collection_exercise_go_live_response = json.load(fp)
        return collection_exercise_go_live_response
