#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>

fd_set master;  // master file descriptor list
fd_set read_fds;  // temp file descriptor list for select()

int main(int argc, char **argv){
    if(argc < 2){
        printf("Usage: %s <portno>", argv[0]);
        exit(1);
    }
    int port = atoi(argv[1]);

    // clear the master and temp sets
    FD_ZERO(&master);
    FD_ZERO(&read_fds);

    // get the listener
    int listener = socket(AF_INET, SOCK_STREAM, 0) ;
    if (listener == -1) {
        perror("socket");
        exit(1);
    }
    return 0;
}