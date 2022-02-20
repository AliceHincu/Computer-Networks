//
// A client sends to the server a string. The server returns the count of spaces in the string.
//

#include <stdio.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

int main() {
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1) {
        perror("Could not open socket!");
        return -1;
    }
    if (setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &(int) {1}, sizeof(int))) {
        perror("setsock");
        return -2;
    }

    struct sockaddr_in server;
    memset(&server, 0, sizeof(server));
    server.sin_port = htons(2021);
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;

    int bind_err = bind(server_socket, (struct sockaddr *) &server, sizeof(server));
    if (bind_err == -1) {
        perror("Could not bind socket");
        return -3;
    }

    if (listen(server_socket, 7) == -1) {
        perror("Could not listen");
        return -1;
    }

    printf("Listening...\n");

    struct sockaddr_in client_addr;
    socklen_t client_addr_len;
    int client_sock = accept(server_socket, (struct sockaddr *) &client_addr, &client_addr_len);
    if (client_sock == -1) {
        perror("Could not connect to client");
        return -4;
    }
    char *client_ip = inet_ntoa(client_addr.sin_addr);
    printf("Acccepted connection! Client:  %s", client_ip);

    return 0;
}