//
// Created by Sakura on 11/4/2021.
//
/*
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

int main() {
    int client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket == -1) {
        perror("Could not open socket");
    }

    struct sockaddr_in server;
    memset(&server, 0, sizeof(server));
    server.sin_port = htons(1234);
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr("172.18.224.1");

    if (connect(client_socket, (struct sockaddr *) &server, sizeof(server)) == -1){
        perror("Could not connect to server!");
        return -1;
    }

    int32_t array[] = {1,2,3,4};
    int32_t size = 4;
    size = htonl(size);
    int32_t nrSentBytes = send(client_socket, &size, sizeof(int32_t), 0);
    if (nrSentBytes != sizeof(int32_t)) {
        perror("Couldn't send size.");
        return -2;
    }

    for(int i=0; i<size; i++){
        array[i] = htonl(array[i]);
        nrSentBytes = send(client_socket, &array[i], sizeof(int32_t), 0);
        if (nrSentBytes != sizeof(int32_t)) {
            perror("Couldn't send number.");
            return -3;
        }
    }

    int32_t sum;
    int nrReadBytes = recv(client_socket, &sum, sizeof(int32_t), 0);
    sum = ntohl(sum);
    if (nrReadBytes != sizeof(int32_t)) {
        perror("Couldn't read sum.");
        return -5;
    }
    printf("%d", sum);
    return 0;
}*/

