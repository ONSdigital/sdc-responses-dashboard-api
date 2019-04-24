import json

import responses
from requests import HTTPError

from app.controllers.survey_controller import get_survey_list
from tests.app import AppContextTestCase


class TestSurveyController(AppContextTestCase):
    with open(AppContextTestCase.test_data_path.joinpath('get_surveys_response.json')) as fp:
        surveys_response = json.load(fp)

    @responses.activate
    def test_get_survey_list_success(self):
        with self.app.app_context():
            responses.add(responses.GET, self.app.config['SURVEY_URL'] + '/surveys', json=self.surveys_response,
                          status=200)

            controller_output = get_survey_list()

        self.assertEqual(self.surveys_response, controller_output)

    @responses.activate
    def test_get_survey_list_auth_failure_raises_http_error(self):
        with self.app.app_context():
            responses.add(responses.GET, self.app.config['SURVEY_URL'] + '/surveys', status=401)

            with self.assertRaises(HTTPError):
                get_survey_list()
