#include <stdio.h>
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
 }