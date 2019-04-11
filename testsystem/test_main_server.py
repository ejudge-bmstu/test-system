import server_settings
import requests
import unittest
import time
import psycopg2
class TestAppBuilder(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.base_url = "http://%(host)s:%(port)s/" % server_settings.rest_settings
        self.connection = psycopg2.connect(**server_settings.db_settings)
        
    def _get_status(self, solution_id):
        request = """SELECT result FROM status WHERE id=(SELECT status_id FROM user_solutions WHERE id=%(solution_id)s)""" 
        params = {'solution_id': solution_id}
        with self.connection.cursor() as cursor:
            cursor.execute(request, params)
            result = cursor.fetchall()
        if len(result) == 0:
            return None
        return result[0]

     
    def test_python_ok(self):
        solution_id = "04cef154-5b6b-11e9-8647-d663bd873d93"
        url = self.base_url + solution_id
        requests.get(url)
        
        time.sleep(3)

        result = self._get_status(solution_id)
        self.assertEqual(result[0], 'Задание выполнено.')
        
     
    def test_python_wrong_answer(self):
        solution_id = "14cef154-5b6b-11e9-8647-d663bd873d93"
        url = self.base_url + solution_id
        requests.get(url)
        
        time.sleep(3)

        result = self._get_status(solution_id)
        self.assertEqual(result[0], 'Неверный ответ.')

     
    def test_python_timeout(self):
        solution_id = "24cef154-5b6b-11e9-8647-d663bd873d93"
        url = self.base_url + solution_id
        requests.get(url)
        
        time.sleep(10)

        result = self._get_status(solution_id)
        self.assertEqual(result[0], 'Прохождение теста превысило максимальное время для задания.')

     
    def test_python_error(self):
        solution_id = "34cef154-5b6b-11e9-8647-d663bd873d93"
        url = self.base_url + solution_id
        requests.get(url)
        
        time.sleep(3)

        result = self._get_status(solution_id)
        self.assertEqual(result[0], 'Ошибка времени выполнения.')

     
    def test_с_ok(self):
        solution_id = "44cef154-5b6b-11e9-8647-d663bd873d93"
        url = self.base_url + solution_id
        requests.get(url)
        
        time.sleep(5)

        result = self._get_status(solution_id)
        self.assertEqual(result[0], 'Задание выполнено.')

     
    def test_с_timeout(self):
        solution_id = "54cef154-5b6b-11e9-8647-d663bd873d93"
        url = self.base_url + solution_id
        requests.get(url)
        
        time.sleep(10)

        result = self._get_status(solution_id)
        self.assertEqual(result[0], 'Прохождение теста превысило максимальное время для задания.')

       
    def test_с_memory_err(self):
        solution_id = "64cef154-5b6b-11e9-8647-d663bd873d93"
        url = self.base_url + solution_id
        requests.get(url)
        
        time.sleep(5)

        result = self._get_status(solution_id)
        self.assertEqual(result[0], 'Прохождение теста превысило максимальный объем памяти задания.')           

     
    def test_c_error(self):
        solution_id = "74cef154-5b6b-11e9-8647-d663bd873d93"
        url = self.base_url + solution_id
        requests.get(url)
        
        time.sleep(5)

        result = self._get_status(solution_id)
        self.assertEqual(result[0], 'Ошибка времени выполнения.')

    
    def test_c_compile_error(self):
        solution_id = "84cef154-5b6b-11e9-8647-d663bd873d93"
        url = self.base_url + solution_id
        requests.get(url)
        
        time.sleep(5)

        result = self._get_status(solution_id)
        self.assertEqual(result[0], 'Ошибка компиляции.')



if __name__ == "__main__":
    unittest.main(exit=False)
