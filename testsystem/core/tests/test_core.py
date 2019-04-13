import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import testcore, settings, builder
import unittest
import shutil


class TestAppBuilder(unittest.TestCase):
    def setUp(self):
        self.docker = testcore.DockerManager()    

    
    def test_run_python_container_ok(self):
        source = """import sys
f = open("/tmp/out.txt", "w")
for x in sys.argv[1:]:
	print(2*int(x), end=' ', file=f)
f.close()"""

        bldr = builder.AppBuilder()
        bldr.assembly(source, "python")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        
        result = self.docker.run_time_container(tag, " python3 source.py 1 2 3", memory_limit=20, mem_swappiness=0, timeout=10)
        self.docker.rm_image("test:test")

        self.assertEqual(result[1], "2 4 6 ")
        
     
    def test_run_python_container_wrong_answer(self):
        source = """import sys
f = open("/tmp/out.txt", "w")
for x in sys.argv[1:]:
	print(3*int(x), end=' ', file=f)
f.close()"""

        bldr = builder.AppBuilder()
        bldr.assembly(source, "python")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        
        result = self.docker.run_time_container(tag, " python3 source.py 1 2 3", memory_limit=100, mem_swappiness=0, timeout=10)
        self.docker.rm_image("test:test")

        self.assertNotEqual(result[1], "2 4 6 ")


     
    def test_run_python_container_timeout(self):
        source = """while 1:
    pass """

        bldr = builder.AppBuilder()
        bldr.assembly(source, "python")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " python3 source.py 1 2 3", memory_limit=20, mem_swappiness=0, timeout=3)
        self.docker.rm_image("test:test")

        self.assertIsNone(result)   


     
    def test_run_python_container_error(self):
        source = """while 1g:
    pass """

        bldr = builder.AppBuilder()
        bldr.assembly(source, "python")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " python3 source.py 1 2 3", memory_limit=20, mem_swappiness=0, timeout=3)
        self.docker.rm_image("test:test")

        self.assertEqual('  File "source.py", line 1\n    while 1g:\n           ^\nSyntaxError: invalid syntax\n', result[1])



     
    def test_run_c_container_ok(self):
        source = """#include <stdio.h>
#include <stdlib.h>  



int main (int argc, char *argv[]) {
 int i=0, tmp;

   FILE *fptr;
fptr = fopen("/tmp/out.txt", "w");


 for (i=1; i< argc; i++) {
tmp = 2 * atoi(argv[i]);
     fprintf(fptr, "%d ", tmp);
 }
fclose(fptr);

 return 0;
 }"""
        
        bldr = builder.AppBuilder()
        a = bldr.assembly(source, "c")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " ./source.out 1 2 3", memory_limit=20, mem_swappiness=0, timeout=10)
        
        self.assertEqual(result[1], "2 4 6 ")


     
    def test_run_c_container_wrong_answer(self):
        source = """#include <stdio.h>
#include <stdlib.h>  



int main (int argc, char *argv[]) {
 int i=0, tmp;

   FILE *fptr;
fptr = fopen("/tmp/out.txt", "w");


 for (i=1; i< argc; i++) {
tmp = 3 * atoi(argv[i]);
     fprintf(fptr, "%d ", tmp);
 }
fclose(fptr);

 return 0;
 }"""
        
        bldr = builder.AppBuilder()
        a = bldr.assembly(source, "c")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " ./source.out 1 2 3", memory_limit=20, mem_swappiness=0, timeout=10)
        
        self.assertNotEqual(result[1], "2 4 6 ")




     
    def test_run_c_container_timeout(self):
        source = """#include <stdio.h>
#include <stdlib.h>  



int main (int argc, char *argv[]) {
 int i=0, tmp;
    while (1) {;};
   FILE *fptr;
fptr = fopen("/tmp/out.txt", "w");


 for (i=1; i< argc; i++) {
tmp = 3 * atoi(argv[i]);
     fprintf(fptr, "%d ", tmp);
 }
fclose(fptr);

 return 0;
 }"""
        
        bldr = builder.AppBuilder()
        a = bldr.assembly(source, "c")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " ./source.out 1 2 3", memory_limit=20, mem_swappiness=0, timeout=5)
        
        self.assertIsNone(result)

     
    def test_run_c_container_over_mem_err(self):
        source = """#include <stdio.h>
#include <stdlib.h>  



int main (int argc, char *argv[]) {
 int i=0, tmp;
    while (1) {char *q = malloc(1024*1024);};
   FILE *fptr;
fptr = fopen("/tmp/out.txt", "w");


 for (i=1; i< argc; i++) {
tmp = 3 * atoi(argv[i]);
     fprintf(fptr, "%d ", tmp);
 }
fclose(fptr);

 return 0;
 }"""
        
        bldr = builder.AppBuilder()
        a = bldr.assembly(source, "c")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " ./source.out 1 2 3", memory_limit=20, mem_swappiness=0, timeout=5)
        
        self.assertEqual(result[0], 137)

     
    def test_run_c_container_min_mem_err(self):
        source = """#include <stdio.h>
#include <stdlib.h>  



int main (int argc, char *argv[]) {
 int i=0, tmp;
    while (1) {char *q = malloc(1024*1024);};
   FILE *fptr;
fptr = fopen("/tmp/out.txt", "w");


 for (i=1; i< argc; i++) {
tmp = 3 * atoi(argv[i]);
     fprintf(fptr, "%d ", tmp);
 }
fclose(fptr);

 return 0;
 }"""
        
        bldr = builder.AppBuilder()
        a = bldr.assembly(source, "c")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " ./source.out 1 2 3", memory_limit=10, mem_swappiness=0, timeout=65)
        
        self.assertEqual(result[0], -137)



     
    def test_run_c_container_seg_fault_err(self):
        source = """#include <stdio.h>
#include <stdlib.h>  
#include <iostream>


int main (int argc, char *argv[]) {
 int i=0, tmp; char *str = "foo";str[0] = 'b';
    
   FILE *fptr;
fptr = fopen("/tmp/out.txt", "w");


 for (i=1; i< argc; i++) {
tmp = 3 * atoi(argv[i]);
     fprintf(fptr, "%d ", tmp);
 }
fclose(fptr);

 return 0;
 }"""
        
        bldr = builder.AppBuilder()
        a = bldr.assembly(source, "cpp")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " ./source.out 1 2 3", memory_limit=20, mem_swappiness=0, timeout=65)
        
        self.assertEqual(result[0], 139)


    def test_run_cpp_container_ok(self):
        source = """#include <stdio.h>
#include <stdlib.h>  



int main (int argc, char *argv[]) {
 int i=0, tmp;

   FILE *fptr;
fptr = fopen("/tmp/out.txt", "w");


 for (i=1; i< argc; i++) {
tmp = 2 * atoi(argv[i]);
     fprintf(fptr, "%d ", tmp);
 }
fclose(fptr);

 return 0;
 }"""
        
        bldr = builder.AppBuilder()
        a = bldr.assembly(source, "c")

        tag = "test:test"
        self.docker.build_image(bldr.docker_file_folder, tag)

        result = self.docker.run_time_container(tag, " ./source.out 1 2 3", memory_limit=20, mem_swappiness=0, timeout=10)
        
        self.assertEqual(result[1], "2 4 6 ")





if __name__ == "__main__":
    unittest.main(exit=False)

    