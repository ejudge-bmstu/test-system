import docker
import subprocess, os
import timeout_decorator
from .settings import answer_filename, answer_dir, answer_len

class DockerManager(object):
    """
    DockerManager is needed for the interaction with docker containers.
    """
    def __init__(self):
        """
   Initialisation of DockerManager.
    :return: None
    """
        self.client = docker.from_env()

    def build_image(self, project, tag, dockerfile = "Dockerfile"):
        """
   Build image with users source code.
    :param project: Dockerfile path.
    :param tag: tag of container.
    :param dockerfile: name of file with container settings.
    """
        self.client.images.build(path = project, tag = tag, dockerfile=dockerfile)

    def rm_image(self, tag):
        """
   Delete certain docker image.
    :param tag: tag of container.
    :return: None
    """
        self.client.images.remove(image=tag, force=True, noprune=False)
        try:
            os.system("""docker rmi $(docker images --filter "dangling=true" -q --no-trunc) -f""")
        except:
            pass


    def _run_container(self, client, run_specs, time):
        """
   Run the container with user code.
    :param client: module that connected to docker API.
    :param run_specs: settings of run command.
    :param time: maximum working time.
    :return: error code and ext information.
    """
        @timeout_decorator.timeout(time)
        def run_container(client, run_specs):
            error = 0
            dn = os.path.dirname(os.path.realpath(__file__))
            mapper_folder = dn + "/" + answer_dir
            try:
                result = client.containers.run(**run_specs, stderr=True, volumes={mapper_folder: {'bind': '/tmp/', 'mode': 'rw'}}).decode("utf-8")
            except docker.errors.ContainerError as exeption:
                error = exeption.exit_status
                result = exeption.stderr.decode("utf-8")
            except docker.errors.APIError as exeption:
                error = -137
                result = "API ERROR. Minimal memory for task error."
            return [error, result]

        return run_container(client, run_specs)


    def _get_answer(self):
        """
   Get answer from users answer file.
    :return: None if file doesnt exist else return user answer.
    """
        path = os.path.dirname(os.path.realpath(__file__)) + "/" + answer_filename
        answer = ""
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            answer = f.read(answer_len)
        try:
            os.unlink(path)
        except:
            print("Unable to delete file.")
        return answer
        






    def run_time_container(self, image_name, command, memory_limit = None, mem_swappiness = None, timeout = None):
        """
   Prepare to run the container.
    :param image_name: name of docker image.
    :param command: command to run image.
    :param memory_limit: maximum working memory of container.
    :param mem_swappiness: maximum of swap memory for container.
    :param timeout: maximum working time.
    :return: error code and ext information.
    """
        timeout_flag = False
        parametres = {'image': image_name, 'command': command}
        if memory_limit is not None:
            mem_limit_dict =  {'mem_limit': memory_limit * 2 ** 20} # pass memory_limit in bytes
        if mem_swappiness is not None:
            mem_swappiness_dict = {'mem_swappiness': mem_swappiness}
            
        run_specs = {**parametres, **mem_limit_dict, **mem_swappiness_dict}

        try:
            result = self._run_container(self.client, run_specs, timeout)
        except timeout_decorator.timeout_decorator.TimeoutError:
            timeout_flag = True
       
        if timeout_flag:
            #stop container
            container_list = self.client.containers.list()
            if len(container_list) > 0:
                self._stop_container(container_list[0])
            return None
        elif result[0] == 0:
            result[1] = self._get_answer()

        return result   


            

    def _stop_container(self, container):
        """Stop the container.
    :param client: container to stop.
    :return: None
    """
        if container is not None:
            container.kill()


        



if __name__ == "__main__":
    a = DockerManager()
    a.run_time_container("a:b", "ls", memory_limit="20M", mem_swappiness=0, timeout=10)
    pass