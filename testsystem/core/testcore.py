import docker
import subprocess, os
import timeout_decorator


class DockerManager(object):
    def __init__(self):
        self.client = docker.from_env()
        self.current_image = None

    def build_image(self, project, tag, dockerfile = "Dockerfile"):
        self.client.images.build(path = project, tag = tag, dockerfile=dockerfile)

    def rm_image(self, tag):
        self.client.images.remove(image=tag, force=True, noprune=False)
        #os.system("""docker rmi $(docker images --filter "dangling=true" -q --no-trunc) -f""")

    
    #@staticmethod
    time_for_timeout = 6
    @timeout_decorator.timeout(time_for_timeout)
    def _run_container(self, client, queue, run_specs):
        try:
            result = client.containers.run(**run_specs, stderr=True, volumes={'/tmp/': {'bind': '/tmp/', 'mode': 'rw'}}).decode("utf-8")
            error = 0
        except docker.errors.ContainerError as exeption:
            error = exeption.exit_status
            result = exeption.stderr.decode("utf-8")
        return [error, result]


    def _get_answer(self):
        path = "/tmp/out.txt"
        buffer_len = 255

        answer = ""
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            answer = f.read(buffer_len)
        os.unlink(path)
        return answer
        






    def run_time_container(self, image_name, command, memory_limit = None, mem_swappiness = None, timeout = None):
        timeout_flag = False
        parametres = {'image': image_name, 'command': command}
        if memory_limit is not None:
            mem_limit_dict =  {'mem_limit': memory_limit*2**20}
        if mem_swappiness is not None:
            mem_swappiness_dict = {'mem_swappiness': mem_swappiness}
            
        run_specs = {**parametres, **mem_limit_dict, **mem_swappiness_dict}

        self.time_for_timeout = timeout

        try:
            result = self._run_container(self.client, None, run_specs)
        except timeout_decorator.timeout_decorator.TimeoutError:
            timeout_flag = True
       
        if timeout_flag:
            #stop container and kill subprocess
            container_list = self.client.containers.list()
            if len(container_list) > 0:
                self._stop_container(container_list[0])
        elif not result[0]:
            result[1] = self._get_answer()
            
            

        if timeout_flag:
            return None
        else:
            return result

            

    def _stop_container(self, container):
        if container is not None:
            container.kill()


        



if __name__ == "__main__":
    a = DockerManager()
    a.run_time_container("a:b", "ls", memory_limit="20M", mem_swappiness=0, timeout=10)
    pass