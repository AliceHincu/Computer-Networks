#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netdb.h>
#include <strings.h>
#include <string.h>

int main() {
    int client_socket = socket(AF_INET, SOCK_DGRAM, 0);
    if(client_socket<0){
        perror("Error on creating socket\n");
        exit(-1);
    }

    struct sockaddr_in server;
    struct hostent *hp = gethostbyname("172.24.160.1");
    if (hp == 0) {
        printf("Unknown host\n");
        exit(-2);
    }

    server.sin_family = AF_INET;
    bcopy((char *)hp->h_addr, (char *)&server.sin_addr, hp->h_length);
    server.sin_port = htons(2021);

    char *message = "mesajTest\n";
    int len = sizeof(struct sockaddr_in);

    int n = sendto(client_socket, message, strlen(message), 0, (struct sockaddr*)&server, len);
    if(n<0){
        perror("Error sendto\n");
        exit(-3);
    }
    return 0;
}
