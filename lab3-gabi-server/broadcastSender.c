#include <sys/socket.h>
#include <stdio.h>
#include <unistd.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>

#define MYPORT 2021

int main(){
    int sender_socket = socket(AF_INET, SOCK_DGRAM, 0);
    char broadcast = '1';

    //    This option is needed on the socket in order to be able to receive broadcast messages
    //   If not set the receiver will not receive broadcast messages in the local network.
    int set_sock_err = setsockopt(sender_socket, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast));
    if (set_sock_err < 0){
        printf("Error in setting broadcast option");
        close(sender_socket);
        return 0;
    }

    struct sockaddr_in receiver_addr;
    socklen_t len = sizeof(struct sockaddr_in);

    char sendMSG[] = "Broadcast message from SLAVE TAG";
    char recv_buff[50] = "";

    // everyone in my lan receives => .255
    receiver_addr.sin_family = AF_INET;
    receiver_addr.sin_port = htons(MYPORT);
    receiver_addr.sin_addr.s_addr = inet_addr("192.168.1.255");

    sendto(sender_socket, sendMSG, strlen(sendMSG+1), 0, (struct sockaddr*)&receiver_addr, len);
    printf("\n\n\tReceived message from Reader is =>  %s", recv_buff);
    close(sender_socket);
    return 0;
}