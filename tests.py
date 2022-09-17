# coding: utf-8

from __future__ import print_function

from datetime import datetime, timedelta
from os import environ
from pprint import PrettyPrinter
from unittest import TestCase
from unittest import main as unittest_main

from webtest import TestApp

from healthplatform_stats_rest_api import rest_api
from healthplatform_stats_rest_api.analytics import sydney


class TestRestApi(TestCase):
    maxDiff = 444444
    app = TestApp(rest_api)

    def test_status(self):
        """Not really needed, but whatever"""
        status_resp = self.app.get("/api/status").json
        for k in status_resp.keys():
            if k.endswith("_version"):
                self.assertEqual(status_resp[k].count("."), 2)

    def test_run(self):
        event_start = datetime(year=2019, month=3, day=11, hour=8, tzinfo=sydney)
        event_end = event_start + timedelta(hours=6, minutes=60)
        actual_output = c.run(event_start, event_end)

        PrettyPrinter(indent=4).pprint(actual_output)

        expected_output = {
            "_out": [
                "survey_tbl#:         000\n"
                "risk_res_tbl#:       000\n"
                "survey_tbl:          000 (excluded using 'createdAt')\n"
                "risk_res_tbl:        000 (excluded using 'createdAt')\n"
                "survey_tbl:          000 (excluded using 'updatedAt')\n"
                "risk_res_tbl:        000 (excluded using 'updatedAt')\n"
                "joint#:              000\n"
                "step1_only_sql#:     000\n"
                "step1_only#:         000\n"
                "step2_only#:         000\n"
                "step3_only#:         000\n"
                "risk_res_ids#:       000\n"
                "event_start_iso:     2019-03-11T08:00:00+11:00 \n"
                "event_end_iso:       2019-03-11T15:00:00+11:00\n"
                "step1_and_2#:        000\n"
                "step1_and_3#:        000\n"
                "step2_and_1#:        000\n"
                "step2_and_3#:        000\n"
                "step3_and_1#:        000\n"
                "step3_and_2#:        000\n\n"
                "The following includes only records that completed all 3 steps:\n"
                "joint_for_pred#:     000\n",
                "",
            ],
            "all_steps": 0,
            "completed": 0,
            "counts": {
                "age_mag": {"Total": 0},
                "behaviour_change": {"Total": 0},
                "client_risk_mag": {"Total": 0},
                "gender": {"Total": 0},
            },
            "email_conversion": 0,
            "emails": 169,
            "join_for_pred_unique_cols": {
                "behaviour_change": {},
                "client_risk_mag": {},
                "perceived_risk_mag": {},
            },
            "joint_for_pred": {
                "age": {},
                "age_mag": {},
                "behaviour_change": {},
                "client_risk": {},
                "client_risk_mag": {},
                "gender": {},
                "perceived_risk": {},
                "perceived_risk_mag": {},
            },
            "some_combination": 0,
            "step1_count": 0,
            "step2_count": 0,
            "step3_count": 0,
            "survey_count": 0.0,
        }

        self.assertSetEqual(set(expected_output.keys()), set(actual_output.keys()))

        if environ.get("TRAVIS"):
            return

        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    unittest_main()
