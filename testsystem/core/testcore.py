import docker
from multiprocessing import Process
import signal


class DockerManager(object):
    def __init__(self):
        self.client = docker.from_env()
        self.current_image = None

    def build_image(self, project, tag, dockerfile = "Dockerfile"):
        self.client.images.build(path = project, tag = tag, dockerfile=dockerfile)

    @staticmethod
    def __run_container(client, return_dict, run_specs):
        result = client.containers.run(**run_specs, stderr=True)
        return_dict.append(result)


    def run_time_container(self, image_name, command, memory_limit = None, mem_swappiness = None, timeout = None):
        return_dict = []

        parametres = {'image': image_name, 'command': command}
        if memory_limit is not None:
            mem_limit_dict =  {'mem_limit': memory_limit}
        if mem_swappiness is not None:
            mem_swappiness_dict = {'mem_swappiness': mem_swappiness}
            
        run_specs = {**parametres, **mem_limit_dict, **mem_swappiness_dict}

        container_instance = Process(target = self.__run_container, args = (self.client, return_dict, run_specs))
        container_instance.start()   



        container_instance.join(timeout)
        if container_instance.is_alive():
            #stop container and kill subprocess
            container_list = self.client.containers.list()
            if len(container_list) > 0:
                self.__stop_container(container_instance, container_list[0])
            else:
                self.__stop_container(container_instance)

        return return_dict
            

    def __stop_container(self, container_instance, container = None):
        if container is not None:
            container.kill()
        container_instance.terminate()
        container_instance.join()

        



if __name__ == "__main__":
    a = DockerManager()
    a.run_time_container("a:b", "ls", memory_limit="20M", mem_swappiness=0, timeout=10)
    pass