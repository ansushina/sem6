#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <arpa/inet.h>
#include <netdb.h>

#define MSG_LEN 256
#define SOCK_ADDR "localhost"
#define SOCK_PORT 9999

#define MAX_CLIENTS 10
int clients[MAX_CLIENTS] = { 0 };


void connectionHandler(unsigned int fd)
{
    struct sockaddr_in addr;
    int addrSize = sizeof(addr);

    int incom = accept(fd, (struct sockaddr*) &addr, (socklen_t*) &addrSize);
    if (incom < 0)
    {
        perror("Error in accept(): ");
        exit(-1);
    }

    printf("\nNew connection: \nfd = %d \nip = %s:%d\n", incom, 
                            inet_ntoa(addr.sin_addr), ntohs(addr.sin_port));

    for (int i = 0; i < MAX_CLIENTS; i++)
    {
        if (clients[i] == 0)
        {
            clients[i] = incom;
            break;
        }
    }

}

void clientHandler(unsigned int fd, unsigned int client_id)
{
    char msg[MSG_LEN];
    memset(msg, 0, MSG_LEN);

    struct sockaddr_in addr;
    int addrSize = sizeof(addr);

    int recvSize = recv(fd, msg, MSG_LEN, 0);
    if (recvSize == 0)
    {
        getpeername(fd, (struct sockaddr*) &addr, (socklen_t*) &addrSize);
        printf("User %d disconnected %s:%d \n", client_id, inet_ntoa(addr.sin_addr), ntohs(addr.sin_port));
        close(fd);
        clients[client_id] = 0;
    }
    else
    {
        msg[recvSize] = '\0';
        printf("Message from %d client: %s\n", client_id, msg);
    }
}


int main(void)
{
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)
    {
        perror("Error in sock\n");
        return sock;
    }

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(SOCK_PORT);
    addr.sin_addr.s_addr = INADDR_ANY; //any address for binding

    if (bind(sock, (struct sockaddr*) &addr, sizeof(addr)) < 0)
    {
        perror("Error in bind\n");
        return -1;
    }
    printf("Server is listening on the %d port!\n", SOCK_PORT);

    if (listen(sock, 3) < 0)
    {
        perror("Error in listen(): ");
        return -1;
    }
    printf("Wait for the connections\n");

    while (1)
    {
        fd_set set; 
        int max_fd = sock;  

        FD_ZERO(&set);
        FD_SET(sock, &set);

        for (int i = 0; i < MAX_CLIENTS; i++)
        {
            if (clients[i] > 0)
            {
                FD_SET(clients[i], &set);
            }

            max_fd = (clients[i] > max_fd) ? (clients[i]) : (max_fd);
        }

        int active_clients_count = select(max_fd + 1, &set, NULL, NULL, NULL);

        if (active_clients_count < 0)
        {
            perror("No active clients");
            return active_clients_count;
        }

        if (FD_ISSET(sock, &set))
        {
            connectionHandler(sock);
        }

        for (int i = 0; i < MAX_CLIENTS; i++)
        {
            int fd = clients[i];
            if ((fd > 0) && FD_ISSET(fd, &set))
            {
                clientHandler(fd, i);
            }
        }
    }

    return 0;
}