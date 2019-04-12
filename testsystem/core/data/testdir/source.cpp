#include <stdio.h>
#include <stdlib.h>  



inttt main (int argc, char *argv[]) {
 int i=0, tmp;

   FILE *fptr;
fptr = fopen("/tmp/out.txt", "w");


 for (i=1; i< argc; i++) {
tmp = 2 * atoi(argv[i]);
     fprintf(fptr, "%d ", tmp);
 }
fclose(fptr);

 return 0;
 }