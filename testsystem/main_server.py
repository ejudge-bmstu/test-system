import json
#from server import FrontServer
from server.front_server import FrontServer
from dbmanager.dbmanager import BDManager
import settings
from queueworker.queueworker import QueueRetriever
from core.testcore import DockerManager
from core.builder import AppBuilder
from core.settings import docker_file_folder, docker_tag, out_file


class MainServer(object):
    def __init__(self):
        self.db_manager = BDManager(settings.dbname, settings.user, settings.password,settings.host, settings.port)
        self.queue_worker = QueueRetriever(settings.dbname, settings.user, settings.password,settings.host, settings.port)
        self.queue = self.queue_worker.queue
        self.docker = DockerManager()
        self.builder = AppBuilder()

        
        self.queue_worker.start()

    def _get_solution(self):
        solution_id = self.queue.get()
        solution = self.db_manager.get_solution(solution_id)
        return solution

    def _assembly_files(self, solution):
        code = solution.answer.program_text
        lang = solution.answer.programming_language
        result = self.builder.assembly(code, lang)
        return result

    def _buid_image(self):
        self.docker.build_image(self.builder.docker_file_folder, docker_tag)

    def _rm_image(self):
        self.docker.rm_image(docker_tag)

    def _run_container(self, solution, command):
        limit = solution.get_limit(solution.answer.programming_language)
        mem_swappiness = 0
        memory_limit = limit.memory_limit
        timeout = limit.time_limit

        err_res = self.docker.run_time_container(docker_tag, command, memory_limit, mem_swappiness, timeout)
        return err_res
    
    def _command_formatter(self, lang):
        if lang == "python":
            return "python3 %s " % (out_file + "py")
        elif lang == "c" or lang == "cpp":
            return "./%s " % (out_file + "out")







    def answer_validation(self, test, answer):
        answer = answer.strip()
        test_str = test.output_data.strip()
        return answer == test_str
        





    def err_code_validation(self, err_res, test, solution):
        status = "err"
        err_code, info = err_res
        user_solution_id = solution.user_solution_id
        test_id = test.test_id


        if err_code is None:
            ext_info = {"info": "Time error."}

        elif err_code == 0:
            if self.answer_validation(test, info):
                status = "ok"
                test_id = None
                ext_info = None
            else:
                ext_info = {"info": "Wrong answer."}
        
        elif err_code == 137:
            ext_info = {"info": "Memory error."}

        elif err_code == -137:
            ext_info = {"info": "Minimal memory error. Docker error."}
            test_id = None

        else:
            ext_info = {"info": "Programm error.\n {}".format(info)}

        self.db_manager.add_status(user_solution_id, status, test_id, ext_info)

        return 0 if status == "ok" else -1





    def _run_tests(self, solution):
        base_command = self._command_formatter(solution.answer.programming_language)
        for test in solution.tests:
            cin = test.input_data
            command = base_command + cin
            err_res = self._run_container(solution, command)
            test_result = self.err_code_validation(err_res, test, solution)
            if test_result == -1:
                break
        return 


    def _build_err_handler(self, information, solution):
        user_solution_id = solution.user_solution_id
        status = "err"
        err_test_id = None
        ext_info = json.dumps({'info': information})

        self.db_manager.add_status(user_solution_id, status, err_test_id, ext_info)
            





    def worker(self):
        solution = self._get_solution()
        
        assembly_err, assembly_info = self._assembly_files(solution)
        if assembly_err:
            self._build_err_handler(assembly_info, solution)
            return 

        self._buid_image()

        self._run_tests(solution)

        self._rm_image()

    
    def start(self): 
        while True:
            self.worker()

#3f94dffc-d71b-4b3e-84d5-96a4778dbc11
if __name__ == "__main__":
    FS = FrontServer()
    FS.start()

    MS = MainServer()
    MS.start()





    
