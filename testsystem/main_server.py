

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

        #self.queue_worker.debug = True

        self.docker = DockerManager()
        self.builder = AppBuilder()

        
        self.queue_worker.start()
    def _get_from_queue(self):
        return self.queue.get()


    def _get_solution(self):
        solution_id = self.queue.get()
        solution = self.db_manager.get_solution(solution_id)
        return solution

    def _assembly_files(self, solution):
        code = solution.answer.program_text
        lang = solution.answer.programming_language
        self.builder.assembly(code, lang)

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


    def answer_validation(self, err_res, test, solution):
        if err_res is None:
            info = {"info": "Time error"}
            self.db_manager.add_status(solution.user_solution_id, "err",test.test_id, info)
            return -1
        elif err_res[0]:
            info = {"info": err_res[1]}
            self.db_manager.add_status(solution.user_solution_id, "err",test.test_id, info)
            return -1
        elif test.output_data != err_res[1].strip():
            info = {"info": "Test Fail"}
            self.db_manager.add_status(solution.user_solution_id, "err",test.test_id, info)
            return -1
        return 0





    def _run_tests(self, solution):
        base_command = self._command_formatter(solution.answer.programming_language)
        for test in solution.tests:
            cin = test.input_data
            command = base_command + cin
            err_res = self._run_container(solution, command)
            test_result = self.answer_validation(err_res, test, solution)
            if test_result == -1:
                return test_result

        self.db_manager.add_status(solution.user_solution_id, "ok",None, """{"info": "QWERTY"}""")
        return 0



    def worker(self):
        solution = self._get_solution()
        #2f94dffc-d71b-4b3e-84d5-96a4778dbc11
        self._assembly_files(solution)
        self._buid_image()

        self._run_tests(solution)

        self._rm_image()

    



if __name__ == "__main__":
    MS = MainServer()
    MS.worker()





    
