import psycopg2
import tablestructures.answers
import tablestructures.solution
import tablestructures.tasklimits
import tablestructures.tests
import uuid

class BDManager():
    def __init__(self,dbname = "ejudge_test",usr = "admin",psw = "admin",host = "localhost", port = "5332"):
        self.connection = psycopg2.connect(database=dbname, user=usr, host=host, password=psw, port=port)
        self.connection.autocommit = True

    def _make_request(self, request, params, insert = False):
        with self.connection.cursor() as cursor:
            cursor.execute(request, params)
            if not insert:
                result = cursor.fetchall()
            else:
                result = None
        return result

    def _get_answer(self, answer_id):
        request = """SELECT programming_language, program_text FROM answers WHERE id = %(answer_id)s"""
        params = {'answer_id': answer_id}
        results = self._make_request(request, params)

        if len(results) == 0:
            return None
        else:
            result = results[0]
            return tablestructures.answers.Answers(result[0], result[1])

    def _get_task_limit(self, task_id, programming_language):
        request = """SELECT memory_limit, time_limit, programming_language FROM task_limits WHERE id = %(task_id)s AND programming_language = %(programming_language)s"""
        params = {'task_id': task_id, 'programming_language': programming_language}
        results = self._make_request(request, params)

        if len(results) == 0:
            return None
        else:
            result = results[0]
            return tablestructures.tasklimits.TaskLimits(result[0], result[1], result[2])

    def _get_tests(self, task_id):
        request = """SELECT input_data, output_data FROM tests WHERE task_id = %(task_id)s"""
        params = {'task_id': task_id}
        results = self._make_request(request, params)

        if len(results) == 0:
            return None
        else:
            return [tablestructures.tests.Tests(test[0], test[1]) for test in results]

    def _get_taskid(self, user_solution_id):
        request = """SELECT task_id FROM user_solutions WHERE id = %(user_solution_id)s"""
        params = {'user_solution_id': user_solution_id}
        results = self._make_request(request, params)

        if len(results) == 0:
            return None
        else:
            return results[0][0]

    def _get_answerid(self, user_solution_id):
        request = """SELECT answer_id FROM user_solutions WHERE id = %(user_solution_id)s"""
        params = {'user_solution_id': user_solution_id}
        results = self._make_request(request, params)

        if len(results) == 0:
            return None
        else:
            return results[0][0]



    def get_solution(self, user_solution_id):
        answer_id = self._get_answerid(user_solution_id)
        task_id = self._get_taskid(user_solution_id)

        answer = self._get_answer(answer_id)
        task_limit = self._get_task_limit(task_id, answer.programming_language)
        tests = self._get_tests(task_id)

        solution = tablestructures.solution.Solution(user_solution_id, answer, tests, task_limit)
        return solution

    def _add_status(self, status_id, result, error_test_id, ext_info = ""):
        request = """INSERT INTO status (id, result, error_test_id, extended_information) VALUES (%(status_id)s,%(result)s,%(error_test_id)s,%(ext_info)s)"""
        params = {'status_id': status_id, 'result': result, 'error_test_id': error_test_id, 'ext_info': ext_info }
        self._make_request(request, params, True)

    def _update_status_id(self, user_solution_id, status_id):
        request = """UPDATE user_solutions SET status_id=%(status_id)s WHERE id=%(user_solution_id)s"""
        params = {'user_solution_id': user_solution_id, 'status_id': status_id}
        self._make_request(request, params, True)

    def add_status(self, user_solution_id, result, error_test_id, ext_info = ""):
        status_id = str(uuid.uuid1())
        self._add_status(status_id,result,error_test_id,ext_info)
        self._update_status_id(user_solution_id, status_id)
        return status_id





if  __name__ == "__main__":
    
    bd = BDManager()
    g = bd.get_solution('e6e1786c-3fe6-4760-8ef4-8785e5be6b06')
    g = 0
    


