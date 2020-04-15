#include <stdio.h>
int main() {

  FILE* fd[2];
  fd[0] = fopen("output.txt","w");
  fd[1] = fopen("output.txt","w");

  int n = 0;

  for(char c = 'a'; c <= 'z'; c++)
  {
      fprintf(fd[n], "%c", c);
      if (n == 0) {
        n = 1;
      } else {
        n = 0;
      }
  }
  fclose(fd[0]);
  fclose(fd[1]);
}