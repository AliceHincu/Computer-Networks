#include <stdio.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdlib.h>
#include <arpa/inet.h>

int main() {
    int server_socket = socket(AF_INET, SOCK_DGRAM,0);
    if (server_socket == -1) {
        perror("Could not open socket");
        exit(-1);
    }
    if (setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &(int) {1}, sizeof(int))) {
        perror("setsock");
        return -2;
    }

    struct sockaddr_in server;
    struct sockaddr_in client;
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(2021);

    if(bind(server_socket, (struct sockaddr*)&server, sizeof(server)) == -1) {
        perror("Could not bind socket");
        exit(-2);
    }

    int nr_bytes;
    char buff[1024];
    socklen_t client_len = sizeof(struct sockaddr_in);
    for(;;){
        printf("Waiting for client conn..\n");
        nr_bytes = recvfrom(server_socket, buff, sizeof(buff), 0, (struct sockaddr*)&client, &client_len);
        printf("Received!");
        if (nr_bytes == 0) {
            printf("client shutdown");
            continue;
        }
        if (nr_bytes == -1) {
            perror("could not read");
            exit(-3);
        }
        char *client_ip = inet_ntoa(client.sin_addr);

        if (nr_bytes > sizeof(buff) - 2) {
            perror("too much data sent");
            exit(-4);
        }
        buff[nr_bytes] = '\0';
        printf("%s sent the text: %s\n", client_ip, buff);

    }
    return 0;
}
