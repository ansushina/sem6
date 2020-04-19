#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <signal.h>
#include <sys/socket.h> 

#define MSG_LEN 256
#define SOCKET_NAME "socket.soc"

int sock;   

void sigint_handler(int signum)
{
    close(sock);
    unlink(SOCKET_NAME);
    printf("Socket was closed by ctrl+c!\n");
}

int main(void)
{
    struct sockaddr addr;

    sock = socket(AF_UNIX, SOCK_DGRAM, 0);
    if (sock < 0)                      
    {
        perror("Can't open socket!");
        exit(1);
    }

    addr.sa_family = AF_UNIX;
    strcpy(addr.sa_data, SOCKET_NAME);  

    if (bind(sock, &addr, sizeof(addr)) < 0) 
    {
        printf("Can't bind name to socket!\n");
        close(sock);
        unlink(SOCKET_NAME);
        perror("Error in bind() ");
        exit(-1);
    }

    printf("\nServer is waiting\n");
    signal(SIGINT, sigint_handler);

    char msg[MSG_LEN];
    while(1)
    {
        int recievedSize = recv(sock, msg, sizeof(msg), 0); 
        if (recievedSize < 0) 
        {
            close(sock);
            unlink(SOCKET_NAME);
            perror("Error in recv()");
            exit(1);
        }

        msg[recievedSize] = 0;
        printf("Client send: %s\n", msg);
    }
    
    printf("Closing socket\n");
    close(sock);
    unlink(SOCKET_NAME);
    return 0;
}
