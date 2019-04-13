import unittest
import dbmanager
import uuid
import sys
import os
testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))


class TestAppBuilder(unittest.TestCase):
    def setUp(self):
        self.bd = dbmanager.BDManager(
            "ejudge_test", "postgres", "0000", port="5433")

    def test_get_answer(self):
        answer_id = "1f94dffc-d71b-4b3e-84d5-96a4778dbc11"
        result = self.bd._get_answer(answer_id)
        self.assertEqual(result.programming_language, "python")
        self.assertEqual(
            result.program_text,
            "import sys\nprint(sys.argv[1:])")

    def test_get_answer_id(self):
        user_solution_id = "1f94dffc-d71b-4b3e-84d5-96a4778dbc11"
        result = self.bd._get_answerid(user_solution_id)
        self.assertEqual(result, "1f94dffc-d71b-4b3e-84d5-96a4778dbc11")

    def test_get_task_id(self):
        user_solution_id = "1f94dffc-d71b-4b3e-84d5-96a4778dbc11"
        result = self.bd._get_taskid(user_solution_id)
        self.assertEqual(result, "1f94dffc-d71b-4b3e-84d5-96a4778dbc11")

    def test_get_tests(self):
        task_id = "2f94dffc-d71b-4b3e-84d5-96a4778dbc11"
        result = self.bd._get_tests(task_id)

        self.assertEqual(result[0].input_data, "1 2 3")
        self.assertEqual(result[0].output_data, "2 4 6")

        self.assertEqual(result[1].input_data, "120")
        self.assertEqual(result[1].output_data, "240")

    def test_get_task_limit(self):
        task_id = "1f94dffc-d71b-4b3e-84d5-96a4778dbc11"
        programming_language = "python"
        result = self.bd._get_task_limit(task_id, programming_language)

        self.assertEqual(result.time_limit, 10)
        self.assertEqual(result.memory_limit, 40)
        self.assertEqual(result.programming_language, "python")

    def test_get_solution_id(self):
        user_solution_id = "1f94dffc-d71b-4b3e-84d5-96a4778dbc11"
        result = self.bd.get_solution(user_solution_id)
        self.assertIsNotNone(result)

    def test_add_status_ok(self):
        temp_uuid = str(uuid.uuid1())
        self.bd._add_status(temp_uuid, "ok", None, """{}""")

        result = self.bd._make_request(
            "SELECT id, result, error_test_id, extended_information FROM status WHERE id=%(uuid_id)s", {
                "uuid_id": temp_uuid})
        result = result[0]
        self.assertEqual(result[0], temp_uuid)
        self.assertEqual(result[1], "ok")
        self.assertEqual(result[2], None)
        self.assertEqual(result[3], {})

    def test_update_solution_id(self):
        user_solution_id = "2f94dffc-d71b-4b3e-84d5-96a4778dbc11"
        updt_uuid = str(uuid.uuid1())

        self.bd._update_status_id(user_solution_id, updt_uuid)

        result = self.bd._make_request(
            "SELECT status_id FROM user_solutions WHERE id=%(user_solution_id)s", {
                "user_solution_id": user_solution_id})
        result = result[0]
        self.assertEqual(result[0], updt_uuid)

    def _test_add_status(self):
        user_solution_id = "2f94dffc-d71b-4b3e-84d5-96a4778dbc11"
        result = "err"
        error_test_id = "2f94dffc-d71b-4b3e-84d5-96a4778dbc11"
        ext = {"gcc": "ERROR!!!"}
        status_id = self.bd.add_status(
            user_solution_id, result, error_test_id, ext)

        result = self.bd._make_request(
            "SELECT status_id FROM user_solutions WHERE id=%(user_solution_id)s", {
                "user_solution_id": user_solution_id})
        result = result[0]
        self.assertEqual(result[0], status_id)

        result = self.bd._make_request(
            "SELECT id, result, error_test_id, extended_information FROM status WHERE id=%(uuid_id)s", {
                "uuid_id": temp_uuid})
        result = result[0]
        self.assertEqual(result[0], status_id)
        self.assertEqual(result[1], "err")
        self.assertEqual(result[2], error_test_id)
        self.assertEqual(result[3], ext)


if __name__ == "__main__":
    unittest.main(exit=False)
