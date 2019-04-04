import docker
from multiprocessing import Process, Queue
import subprocess, os

class DockerManager(object):
    def __init__(self):
        self.client = docker.from_env()
        self.current_image = None

    def build_image(self, project, tag, dockerfile = "Dockerfile"):
        self.client.images.build(path = project, tag = tag, dockerfile=dockerfile)

    def rm_image(self, tag):
        self.client.images.remove(image=tag, force=True, noprune=False)
        #os.system("""docker rmi $(docker images --filter "dangling=true" -q --no-trunc) -f""")


    @staticmethod
    def _run_container(client, queue, run_specs):
        try:
            result = client.containers.run(**run_specs, stderr=True).decode("utf-8")
            error = 0
        except docker.errors.ContainerError as exeption:
            error = exeption.exit_status
            result = exeption.stderr.decode("utf-8")
        queue.put((error, result))


    def run_time_container(self, image_name, command, memory_limit = None, mem_swappiness = None, timeout = None):
        queue = Queue()

        parametres = {'image': image_name, 'command': command}
        if memory_limit is not None:
            mem_limit_dict =  {'mem_limit': memory_limit}
        if mem_swappiness is not None:
            mem_swappiness_dict = {'mem_swappiness': mem_swappiness}
            
        run_specs = {**parametres, **mem_limit_dict, **mem_swappiness_dict}

        container_instance = Process(target = self._run_container, args = (self.client, queue, run_specs))
        container_instance.start()   



        container_instance.join(timeout)
        if container_instance.is_alive():
            #stop container and kill subprocess
            container_list = self.client.containers.list()
            if len(container_list) > 0:
                self._stop_container(container_instance, container_list[0])
            else:
                self._stop_container(container_instance)
            

        if queue.qsize() == 0:
            return None
        else:
            return queue.get()

            

    def _stop_container(self, container_instance, container = None):
        if container is not None:
            container.kill()
        container_instance.terminate()
        container_instance.join()

        



if __name__ == "__main__":
    a = DockerManager()
    a.run_time_container("a:b", "ls", memory_limit="20M", mem_swappiness=0, timeout=10)
    pass