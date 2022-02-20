#include <sys/socket.h>
#include <stdio.h>
#include <unistd.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>

#define MYPORT 2021

int main(){
    int receiver_socket = socket(AF_INET, SOCK_DGRAM, 0);
    char broadcast = '1';

    //    This option is needed on the socket in order to be able to receive broadcast messages
    //   If not set the receiver will not receive broadcast messages in the local network.
    int set_sock_err = setsockopt(receiver_socket, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast));
    if (set_sock_err < 0){
        printf("Error in setting broadcast option");
        close(receiver_socket);
        return 0;
    }
    if (setsockopt(receiver_socket, SOL_SOCKET, SO_REUSEADDR, &(int) {1}, sizeof(int))) {
        perror("setsock");
        close(receiver_socket);
        return -2;
    }

    struct sockaddr_in receiver_addr;
    struct sockaddr_in sender_addr;
    int len = sizeof(struct sockaddr_in);

    char recvbuff[50];
    int recvbufflen = 50;
    char sendMSG[]= "Broadcast message from READER";

    // everyone in my lan receives => .255
    receiver_addr.sin_family = AF_INET;
    receiver_addr.sin_port = htons(MYPORT);
    receiver_addr.sin_addr.s_addr = INADDR_ANY;

    if(bind(receiver_socket, (struct sockaddr*)&receiver_addr, len) < 0){
        printf("Error in binding");
        close(receiver_socket);
        return 0;
    }

    recvfrom(receiver_socket, recvbuff, recvbufflen, 0, (struct sockaddr *)&sender_addr, &len);
    printf("\nReceived Message is : %s", recvbuff);

    if(sendto(receiver_socket, sendMSG, strlen(sendMSG+1), 0, (struct sockaddr*)&sender_addr, sizeof(sender_addr)) < 0){
        printf("Error in sending");
        close(receiver_socket);
        return 0;
    }
    else
        printf("\n\tREADER sends the broadcast message Successfully");

    close(receiver_socket);
    return 0;
}