#include <stdio.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <pthread.h>

// gcc -Wall main.c
// THIS IS THE SERVER
int client_sock;
pthread_mutex_t client_sock_mtx;
pthread_mutex_t users_mtx;

typedef struct {
    char ip[64];
    char name[64];
} UserInfo;

typedef struct{
    UserInfo users_data[100];
    int len;
}Users;

typedef struct {
    int sock;
    char *ip;
} ClientData;

Users users;

/*
void time_out(int signal) {
    int32_t res = htonl(-1);

    printf("Time out.\n");

    send(client_sock, &res, sizeof(int32_t), 0);

    if (close(client_sock)){
        perror("Could not close socket.");
        exit(-6);
    }
}*/

int does_user_exist(char *ip){
    pthread_mutex_lock(&users_mtx);
    for (int i=0; i< users.len; i++){
        if (strcmp(users.users_data[i].ip, ip) == 0){
            pthread_mutex_unlock(&users_mtx);
            return 1;
        }
    }
    pthread_mutex_unlock(&users_mtx);
    return 0;
}

int add_user(char *ip, char *username) {
    pthread_mutex_lock(&users_mtx);
    if (users.len == 99) {
        pthread_mutex_unlock(&users_mtx);
        return 1;
    }
    if(strlen(ip) > 63) {
        pthread_mutex_unlock(&users_mtx);
        return 2;
    }

    strcpy(users.users_data[users.len].ip, ip);

    if(strlen(username) > 63) {
        pthread_mutex_unlock(&users_mtx);
        return 3;
    }

    strcpy(users.users_data[users.len++].name, username);
    pthread_mutex_unlock(&users_mtx);
    return 0;
}

char *get_username(char *ip){
    pthread_mutex_lock(&users_mtx);
    for(int i=0; i<users.len;i++){
        if(strcmp(users.users_data[i].ip, ip) == 0){
            pthread_mutex_unlock(&users_mtx);
            return users.users_data[i].name;
        }
    }
    pthread_mutex_unlock(&users_mtx);
    return "";
}

void treat_client_conn(ClientData *client_data){
    char res[1024];
    memset(res, 0, sizeof(res));
    int _ = recv(client_data->sock, (void *)res, sizeof(res), 0);

    if (strlen(res) == 0){
        perror("String is empty");
        exit(-6);
    }

    printf("User connected: %s on IP: %s\n", res, client_data->ip);

    if(!does_user_exist(client_data->ip)) {
        int errno = add_user(client_data->ip, res);
        switch (errno) {
            case 1:{
                puts("No more space");
                break;
            }
            case 2:{
                puts("IP too long!");
                break;
            }
            case 3:{
                puts("Username too long!");
                break;
            }
            case 0:
                break;
            default:{
                puts("something else");
                break;
            }
        }
        if (errno == 0)
            printf("User %s successfully added for IP:%s\n", res, client_data->ip);

        close(client_data->sock);
        pthread_mutex_unlock(&client_sock_mtx);
        return;
    }
    char *username = get_username(client_data->ip);
    printf("%s said: %s\n", username, res);

    close(client_data->sock);
    pthread_mutex_unlock(&client_sock_mtx);
}


int main() {
    if(pthread_mutex_init(&client_sock_mtx, NULL) != 0){
        perror("error initializing mutex");
        return -8;
    }
    if(pthread_mutex_init(&users_mtx, NULL) != 0){
        perror("error initializing mutex");
        return -8;
    }

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("Could not open socket");
        return -3;
    }


    if(setsockopt(sock, SOL_SOCKET, SO_REUSEADDR , &(int){1}, sizeof(int))){
        perror("setsock");
        return -10;
    }

    struct sockaddr_in server; // <netinet/ip.h>
    memset(&server, 0, sizeof(server));
    server.sin_port = htons(1234);
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;

    int bind_err = bind(sock, (struct sockaddr *)&server, sizeof(server));
    if (bind_err == -1){
        perror("Could not bind socket");
        return -2;
    }

    if(listen(sock, 7) == -1){
        perror("Could not listen");
        return -1;
    }

    struct sockaddr_in client_addr;
    socklen_t client_addr_len;

    printf("Listening...\n");

    pthread_t threads[30];

    while(1) {
        printf("Listening for new connection...\n");
        pthread_mutex_lock(&client_sock_mtx);
        client_sock = accept(sock, (struct sockaddr *) &client_addr, &client_addr_len);

        int empty_thread_index = 30;
        for(int i=0; i<30;i++){
            if(threads[i] == -1){
                empty_thread_index = i;
                break;
            }
        }
        if(empty_thread_index == 30){
            perror("all threads busy");
            continue;
        }

        char *client_ip = inet_ntoa(client_addr.sin_addr);
        ClientData client_data = {
                .sock= client_sock,
                .ip= client_ip
        };
        int err_code = pthread_create(&threads[empty_thread_index], NULL, (void*) treat_client_conn, (void*)&client_data);
        if (err_code != 0){
            perror("Couldn't spawn thread");
            exit(err_code);
        }

        if (client_sock == -1) {
            perror("Could not connect to client");
            return -4;
        }

        if(pthread_join(threads[empty_thread_index], 0) != 0) {
            perror("Could not join thread");
            return -7;
        } else {
            threads[empty_thread_index] = -1;
        }

    }
    if(pthread_mutex_destroy(&client_sock_mtx) != 0){
        perror("Could not destroy mutex");
        return -8;
    }
    if(pthread_mutex_destroy(&users_mtx) != 0){
        perror("Could not destroy mutex");
        return -8;
    }
    return 0;
}