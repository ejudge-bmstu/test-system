import psycopg2
import tablestructures

class BDManager():
    def __init__(self,dbname = "Railway",usr = "postgres",psw = "0000",host = "localhost"):
        self.connection = psycopg2.connect(database=dbname, user=usr, host=host, password=psw)


    def __make_request(self, request, params):
        with self.connection.cursor() as cursor:
            cursor.execute(request, params)
            result = cursor.fetchall()
        return result

    def __get_answer(self, answer_id):
        request = """SELECT * FROM answers WHERE id = %(answer_id)s"""
        params = {'answer_id': answer_id}
        results = self.__make_request(request, params)

        if len(results) == 0:
            return None
        else:
            result = results[0]
            return tablestructures.answers.Answers(result[1], result[2])

    def __get_task_limit(self, task_id, programming_language):
        request = """SELECT * FROM task_limits WHERE id = %(task_id)s AND programming_language = %(programming_language)s"""
        params = {'task_id': task_id, 'programming_language': programming_language}
        results = self.__make_request(request, params)

        if len(results) == 0:
            return None
        else:
            result = results[0]
            return tablestructures.tasklimits.TaskLimits(result[1], result[2], result[3])

    def __get_tests(self, task_id):
        request = """SELECT * FROM tests WHERE id = %(task_id)s"""
        params = {'task_id': task_id}
        results = self.__make_request(request, params)

        if len(results) == 0:
            return None
        else:
            return [tablestructures.tests.Tests(test[1], test[2]) for test in results]

    def __get_taskid(self, user_solution_id):
        request = """SELECT task_id FROM user_solutions WHERE id = %(user_solution_id)s"""
        params = {'user_solution_id': user_solution_id}
        results = self.__make_request(request, params)

        if len(results) == 0:
            return None
        else:
            return results[0]

    def __get_answerid(self, user_solution_id):
        request = """SELECT answer_id FROM user_solutions WHERE id = %(user_solution_id)s"""
        params = {'user_solution_id': user_solution_id}
        results = self.__make_request(request, params)

        if len(results) == 0:
            return None
        else:
            return results[0]



    def get_solution(self, user_solution_id):
        answer_id = self.__get_answerid(user_solution_id)
        task_id = self.__get_taskid(user_solution_id)

        answer = self.__get_answer(answer_id)
        task_limit = self.__get_task_limit(task_id, answer.programming_language)
        tests = self.__get_tests(task_id)

        solution = tablestructures.solution.Solution(user_solution_id, answer, tests, task_limit)
        return solution



        


