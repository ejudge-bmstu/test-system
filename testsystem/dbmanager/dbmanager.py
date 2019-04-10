import psycopg2
from .tablestructures import answers, solution, tasklimits, tests
import uuid

class BDManager():
    """
    BDManager is needed for the interaction of the main server and the database.
    """
    def __init__(self, db_settings):
        """
   Initialisation of BDManager.
    :param db_settings: setting of database to connect.
    :return: None
    """
        self.connection = psycopg2.connect(**db_settings)
        self.connection.autocommit = True

    def _make_request(self, request, params, insert = False):
        """
    Method to make custom request to database.
    :param request: body of SQL-request without parameters.
    :param params: parameters for SQL-request.
    :param delete: Is request for insert row.
    :return: None if request for insert row else return result of request.
    """
        with self.connection.cursor() as cursor:
            cursor.execute(request, params)
            if not insert:
                result = cursor.fetchall()
            else:
                result = None
        return result

    def _get_answer(self, answer_id):
        """
    Method to get answer from database.
    :param answer_id: answer id of solution.
    :return: None if no results else return result in Answer struct.
    """
        request = """SELECT programming_language, program_text FROM answers WHERE id = %(answer_id)s"""
        params = {'answer_id': answer_id}
        results = self._make_request(request, params)

        if len(results) == 0:
            return None
        else:
            result = results[0]
            return answers.Answers(result[0], result[1])

    def _get_task_limit(self, task_id, programming_language):
        """
    Method to get task limit from database.
    :param task_id: task id of solution.
    :param programming_language: programming language of solution.
    :return: None if no results else return result in TaskLimits struct.
    """
        request = """SELECT memory_limit, time_limit, programming_language FROM task_limits WHERE task_id = %(task_id)s AND programming_language = %(programming_language)s"""
        params = {'task_id': task_id, 'programming_language': programming_language}
        results = self._make_request(request, params)

        if len(results) == 0:
            return None
        else:
            result = results[0]
            return tasklimits.TaskLimits(result[0], result[1], result[2])

    def _get_tests(self, task_id):
        """
    Method to get tests from database.
    :param task_id: task id for tests.
    :return: None if no results else return result in Tests struct.
    """
        request = """SELECT input_data, output_data, id FROM tests WHERE task_id = %(task_id)s"""
        params = {'task_id': task_id}
        results = self._make_request(request, params)

        if len(results) == 0:
            return None
        else:
            return [tests.Tests(test[0], test[1], test[2]) for test in results]

    def _get_taskid(self, user_solution_id):
        """
    Method to get task id from database.
    :param user_solution_id: user solution id.
    :return: None if no results else return task id.
    """
        request = """SELECT task_id FROM user_solutions WHERE id = %(user_solution_id)s"""
        params = {'user_solution_id': user_solution_id}
        results = self._make_request(request, params)

        if len(results) == 0:
            return None
        else:
            return results[0][0]

    def _get_answerid(self, user_solution_id):
        """
    Method to get answer id from database.
    :param user_solution_id: user solution id.
    :return: None if no results else return answer id.
    """
        request = """SELECT answer_id FROM user_solutions WHERE id = %(user_solution_id)s"""
        params = {'user_solution_id': user_solution_id}
        results = self._make_request(request, params)

        if len(results) == 0:
            return None
        else:
            return results[0][0]



    def get_solution(self, user_solution_id):
        """
    Method to get solution id from database.
    :param user_solution_id: user solution id.
    :return: None if no results else return solution id.
    """
        answer_id = self._get_answerid(user_solution_id)
        task_id = self._get_taskid(user_solution_id)

        answer = self._get_answer(answer_id)
        task_limit = self._get_task_limit(task_id, answer.programming_language)
        tests = self._get_tests(task_id)

        sol = solution.Solution(user_solution_id, answer, tests, task_limit)
        return sol

    def _add_status(self, status_id, result, error_test_id, ext_info = ""):
        """
    Method to create SQL request to add status of solution.
    :param status_id: status id.
    :param result: result of solution.
    :param error_test_id: id of test where solution got error.
    :param ext_info: extended information.
    :return: None
    """
        request = """INSERT INTO status (id, result, error_test_id, extended_information) VALUES (%(status_id)s,%(result)s,%(error_test_id)s,%(ext_info)s)"""
        params = {'status_id': status_id, 'result': result, 'error_test_id': error_test_id, 'ext_info': ext_info }
        self._make_request(request, params, True)

    def _update_status_id(self, user_solution_id, status_id):
        """
    Method to create SQL request to update status id of solution.
    :param user_solution_id: user solution id.
    :param status_id: status id.
    :return: None
    """
        request = """UPDATE user_solutions SET status_id=%(status_id)s WHERE id=%(user_solution_id)s"""
        params = {'user_solution_id': user_solution_id, 'status_id': status_id}
        self._make_request(request, params, True)

    def add_status(self, user_solution_id, result, error_test_id, ext_info = ""):
        """
    Method to add status of solution.
    :param status_id: status id.
    :param result: result of solution.
    :param error_test_id: id of test where solution got error.
    :param ext_info: extended information.
    :return: new id of created status
    """
        status_id = str(uuid.uuid1())
        self._add_status(status_id,result,error_test_id,ext_info)
        self._update_status_id(user_solution_id, status_id)
        return status_id





if  __name__ == "__main__":
    
    bd = BDManager()
    g = bd.get_solution('e6e1786c-3fe6-4760-8ef4-8785e5be6b06')
    g = 0
    


