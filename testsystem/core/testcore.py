import docker
from multiprocessing import Process



class DockerManager(object):
    def __init__(self):
        self.client = docker.from_env()
        self.current_image = None

    def build_image(self, project, tag, dockerfile = "Dockerfile"):
        self.client.images.build(path = project, tag = tag, dockerfile=dockerfile)

    @staticmethod
    def __run_container(container, return_dict, image_name, command, memory_limit = None, mem_swappiness = None):
        run_specs = {'image': image_name, 'command': command}
        if memory_limit is not None:
            run_specs += {'mem_linit': memory_limit}
        if mem_swappiness is not None:
            run_specs += {'mem_swappiness': mem_swappiness}
        result = client.containers.run(run_specs, stderr=True)
        return_dict.append(result)

    def run_time_container(self, image_name, command, memory_limit = None, mem_swappiness = None, timeout = None):
        return_dict = []
        container_instance = Process(target = self.__run_container, args = (self.client, return_dict, image_name, command, memory_limit, mem_swappiness))
        container_instance.run()

        container_instance.join(timeout)
        if container_instance.is_alive():
            #stop container and kill subprocess
            self.client.containers.stop_container(0)
            container_instance.terminate()
            container_instance.join()
            

    def stop_container(self):
        pass

        



