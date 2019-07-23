import json
from datetime import datetime
from random import SystemRandom

from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
app.env = 'development'
CORS(app)


@app.route(
    '/reporting-api/v1/response-dashboard/survey/<survey_id>/collection-exercise/<collection_exercise_id>',
    methods=['GET'])
def get_report(survey_id, collection_exercise_id):
    rand_gen = SystemRandom()

    sample_size = rand_gen.randint(100, 1000)
    accounts_enrolled = rand_gen.randint(0, sample_size)
    accounts_pending = rand_gen.randint(0, (sample_size - accounts_enrolled) // 10)
    downloads = rand_gen.randint(0, accounts_enrolled)
    uploads = rand_gen.randint(0, downloads)

    response = {
        'metadata': {
            'collectionExerciseId': collection_exercise_id,
            'timeUpdated': datetime.now().timestamp()
        },
        'report': {
            'inProgress': downloads - uploads,
            'accountsPending': accounts_pending,
            'accountsEnrolled': accounts_enrolled,
            'notStarted': sample_size - downloads,
            'completed': uploads,
            'sampleSize': sample_size
        }
    }

    return Response(json.dumps(response), content_type='application/json')


@app.route('/collectionexercises/<ce_id>/events', methods=['GET'])
def get_collection_exercise_events(ce_id):
    return Response(
        json.dumps(
            [
                {
                    "id": "f924633a-573e-4bb8-9a44-bd571d517fa9",
                    "collectionExerciseId": ce_id,
                    "tag": "employment",
                    "timestamp": "2018-06-15T00:00:00.000Z"
                },
                {
                    "id": "6b5f9a2f-7b5c-40c5-818f-07c8904418c5",
                    "collectionExerciseId": ce_id,
                    "tag": "exercise_end",
                    "timestamp": "2020-08-31T00:00:00.000Z"
                },
                {
                    "id": "7f530007-6213-44d7-99f7-08fda2792946",
                    "collectionExerciseId": ce_id,
                    "tag": "go_live",
                    "timestamp": "2018-06-25T00:00:00.000Z"
                },
                {
                    "id": "bed8307d-df6a-403c-b2f0-04c219bc88b4",
                    "collectionExerciseId": ce_id,
                    "tag": "mps",
                    "timestamp": "2018-06-19T00:00:00.000Z"
                },
                {
                    "id": "8b5c3766-5658-46ea-ba48-0187b54f997a",
                    "collectionExerciseId": ce_id,
                    "tag": "ref_period_end",
                    "timestamp": "2018-06-30T00:00:00.000Z"
                },
                {
                    "id": "ca3ae637-0195-4423-bc75-aa11ab7c86d5",
                    "collectionExerciseId": ce_id,
                    "tag": "ref_period_start",
                    "timestamp": "2018-06-01T00:00:00.000Z"
                },
                {
                    "id": "ad5836b0-7159-47f1-8273-a247e3e07032",
                    "collectionExerciseId": ce_id,
                    "tag": "reminder",
                    "timestamp": "2018-07-10T00:00:00.000Z"
                },
                {
                    "id": "de82fff7-39ad-4355-be45-608f4d03b54a",
                    "collectionExerciseId": ce_id,
                    "tag": "return_by",
                    "timestamp": "2018-07-07T00:00:00.000Z"
                }
            ]
        )
    )


@app.route('/surveys', methods=['GET'])
def get_surveys():
    return Response(
        json.dumps(
            [
                {
                    "id": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87",
                    "shortName": "BRES",
                    "longName": "Business Register and Employment Survey",
                    "surveyRef": "221",
                    "legalBasis": "Statistics of Trade Act 1947",
                    "legalBasisRef": "STA1947",
                    "surveyType": "Business"
                },
                {
                    "id": "04dbb407-4438-4f89-acc4-53445d75330c",
                    "shortName": "AOFDI",
                    "longName": "Annual Outward Foreign Direct Investment Survey",
                    "surveyRef": "063",
                    "legalBasis": "Statistics of Trade Act 1947",
                    "legalBasisRef": "STA1947",
                    "surveyType": "Business"
                },
                {
                    "id": "04dbb407-4438-4f89-acc4-53445d753111",
                    "shortName": "QBS",
                    "longName": "Quarterly Business Survey",
                    "surveyRef": "064",
                    "legalBasis": "Statistics of Trade Act 1947",
                    "legalBasisRef": "STA1947",
                    "surveyType": "Business"
                },
                {
                    "id": "56dbb407-4438-4f89-acc4-53445d753111",
                    "shortName": "LMS",
                    "longName": "Labour Market Survey",
                    "surveyRef": "999",
                    "surveyType": "Social",
                    "legalBasis": "Statistics of Trade Act 1947",
                    "legalBasisRef": "STA1947"
                }
            ]
        )
    )


@app.route('/collectionexercises', methods=['GET'])
def get_collection_exercises():
    return Response(
        json.dumps(
            [
                {
                    "id": "14fb3e68-4dca-46db-bf49-04b84e07e77c",
                    "surveyId": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87",
                    "name": "Business Register an",
                    "actualExecutionDateTime": None,
                    "scheduledExecutionDateTime": "2017-09-10T23:00:00.000Z",
                    "scheduledStartDateTime": "2017-09-11T23:00:00.000Z",
                    "actualPublishDateTime": None,
                    "periodStartDateTime": "2017-05-14T23:00:00.000Z",
                    "periodEndDateTime": "2017-11-17T22:59:59.000Z",
                    "scheduledReturnDateTime": "2017-10-06T00:00:00.000Z",
                    "scheduledEndDateTime": "2018-06-29T23:00:00.000Z",
                    "executedBy": None,
                    "state": "READY_FOR_LIVE",
                    "caseTypes": [
                        {
                            "actionPlanId": "e71002ac-3575-47eb-b87f-cd9db92bf9a7",
                            "sampleUnitType": "B"
                        },
                        {
                            "actionPlanId": "0009e978-0932-463b-a2a1-b45cb3ffcb2a",
                            "sampleUnitType": "BI"
                        }
                    ],
                    "exerciseRef": "201705",
                    "userDescription": "May 2017",
                    "created": None,
                    "updated": None,
                    "deleted": False,
                    "validationErrors": None
                },
                {
                    "id": "14fb3e68-4dca-46db-bf49-04b84e07e7cc",
                    "surveyId": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87",
                    "name": "Business Register an",
                    "actualExecutionDateTime": None,
                    "scheduledExecutionDateTime": "2017-09-10T23:00:00.000Z",
                    "scheduledStartDateTime": "2017-09-11T23:00:00.000Z",
                    "actualPublishDateTime": None,
                    "periodStartDateTime": "2017-05-14T23:00:00.000Z",
                    "periodEndDateTime": "2017-11-19T22:59:59.000Z",
                    "scheduledReturnDateTime": "2017-10-06T00:00:00.000Z",
                    "scheduledEndDateTime": "2018-06-29T23:00:00.000Z",
                    "executedBy": None,
                    "state": "LIVE",
                    "caseTypes": [
                        {
                            "actionPlanId": "e71002ac-3575-47eb-b87f-cd9db92bf9a7",
                            "sampleUnitType": "B"
                        },
                        {
                            "actionPlanId": "0009e978-0932-463b-a2a1-b45cb3ffcb2a",
                            "sampleUnitType": "BI"
                        }
                    ],
                    "exerciseRef": "201709",
                    "userDescription": "September 2017",
                    "created": None,
                    "updated": None,
                    "deleted": False,
                    "validationErrors": None
                },
                {
                    "id": "14fb3e68-4dca-46db-bf49-04b84e07e777",
                    "surveyId": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87",
                    "name": "Business Register an",
                    "actualExecutionDateTime": None,
                    "scheduledExecutionDateTime": "2017-09-10T23:00:00.000Z",
                    "scheduledStartDateTime": "2017-09-11T23:00:00.000Z",
                    "actualPublishDateTime": None,
                    "periodStartDateTime": "2018-01-03T23:00:00.000Z",
                    "periodEndDateTime": "2018-03-17T22:59:59.000Z",
                    "scheduledReturnDateTime": "2017-10-06T00:00:00.000Z",
                    "scheduledEndDateTime": "2018-06-29T23:00:00.000Z",
                    "executedBy": None,
                    "state": "LIVE",
                    "caseTypes": [
                        {
                            "actionPlanId": "e71002ac-3575-47eb-b87f-cd9db92bf9a7",
                            "sampleUnitType": "B"
                        },
                        {
                            "actionPlanId": "0009e978-0932-463b-a2a1-b45cb3ffcb2a",
                            "sampleUnitType": "BI"
                        }
                    ],
                    "exerciseRef": "201801",
                    "userDescription": "January 2018",
                    "created": None,
                    "updated": None,
                    "deleted": False,
                    "validationErrors": None
                },
                {
                    "id": "14fb3e68-4dca-46db-bf49-04b84e07e799",
                    "surveyId": "04dbb407-4438-4f89-acc4-53445d75330c",
                    "name": "Business Register an",
                    "actualExecutionDateTime": None,
                    "scheduledExecutionDateTime": "2017-09-10T23:00:00.000Z",
                    "scheduledStartDateTime": "2017-09-11T23:00:00.000Z",
                    "actualPublishDateTime": None,
                    "periodStartDateTime": "2017-09-14T23:00:00.000Z",
                    "periodEndDateTime": "2017-09-15T22:59:59.000Z",
                    "scheduledReturnDateTime": "2017-10-06T00:00:00.000Z",
                    "scheduledEndDateTime": "2018-06-29T23:00:00.000Z",
                    "executedBy": None,
                    "state": "READY_FOR_LIVE",
                    "caseTypes": [
                        {
                            "actionPlanId": "e71002ac-3575-47eb-b87f-cd9db92bf9a7",
                            "sampleUnitType": "B"
                        },
                        {
                            "actionPlanId": "0009e978-0932-463b-a2a1-b45cb3ffcb2a",
                            "sampleUnitType": "BI"
                        }
                    ],
                    "exerciseRef": "201712",
                    "userDescription": "March 2017",
                    "created": None,
                    "updated": None,
                    "deleted": False,
                    "validationErrors": None
                },
                {
                    "id": "14fb3e68-4dca-46db-bf49-04b84e07e77c",
                    "surveyId": "04dbb407-4438-4f89-acc4-53445d75330c",
                    "name": "Business Register an",
                    "actualExecutionDateTime": None,
                    "scheduledExecutionDateTime": "2017-09-10T23:00:00.000Z",
                    "scheduledStartDateTime": "2017-09-11T23:00:00.000Z",
                    "actualPublishDateTime": None,
                    "periodStartDateTime": "2017-09-14T23:00:00.000Z",
                    "periodEndDateTime": "2017-09-15T22:59:59.000Z",
                    "scheduledReturnDateTime": "2017-10-06T00:00:00.000Z",
                    "scheduledEndDateTime": "2018-06-29T23:00:00.000Z",
                    "executedBy": None,
                    "state": "CREATED",
                    "caseTypes": [
                        {
                            "actionPlanId": "e71002ac-3575-47eb-b87f-cd9db92bf9a7",
                            "sampleUnitType": "B"
                        },
                        {
                            "actionPlanId": "0009e978-0932-463b-a2a1-b45cb3ffcb2a",
                            "sampleUnitType": "BI"
                        }
                    ],
                    "exerciseRef": "201812",
                    "userDescription": "You Can't See Me",
                    "created": None,
                    "updated": None,
                    "deleted": False,
                    "validationErrors": None
                },
                {
                    "id": "14fb3e68-4dca-46db-bf49-04b84e07e999",
                    "surveyId": "04dbb407-4438-4f89-acc4-53445d753111",
                    "name": "Quarterly Business Survey",
                    "actualExecutionDateTime": None,
                    "scheduledExecutionDateTime": "2017-09-10T23:00:00.000Z",
                    "scheduledStartDateTime": "2017-09-11T23:00:00.000Z",
                    "actualPublishDateTime": None,
                    "periodStartDateTime": "2017-09-14T23:00:00.000Z",
                    "periodEndDateTime": "2017-09-15T22:59:59.000Z",
                    "scheduledReturnDateTime": "2017-10-06T00:00:00.000Z",
                    "scheduledEndDateTime": "2018-06-29T23:00:00.000Z",
                    "executedBy": None,
                    "state": "LIVE",
                    "caseTypes": [
                        {
                            "actionPlanId": "e71002ac-3575-47eb-b87f-cd9db92bf9a7",
                            "sampleUnitType": "B"
                        },
                        {
                            "actionPlanId": "0009e978-0932-463b-a2a1-b45cb3ffcb2a",
                            "sampleUnitType": "BI"
                        }
                    ],
                    "exerciseRef": "201712",
                    "userDescription": "December 2017",
                    "created": None,
                    "updated": None,
                    "deleted": False,
                    "validationErrors": None
                }
            ]
        )
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
