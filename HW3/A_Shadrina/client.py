# -*- coding: utf-8 -*-
import socket
import requests
import time

num_of_iter = 1000

# SERVER_HOST = 'localhost'
# SERVER_PORT = 8090

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000


def socket_client():
    client_socket = socket.socket()
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    for i in range(num_of_iter):
        # client_socket.send(i.to_bytes(4, 'little'))  # echo
        client_socket.send((17).to_bytes(4, 'little'))  # fibonacci
        response = client_socket.recv(4096)
        # print(f'{response} was received')

    client_socket.close()


def request_client():
    for _ in range(num_of_iter):
        # r = requests.get(f'http://{SERVER_HOST}:{SERVER_PORT}/echo')
        r = requests.get(f'http://{SERVER_HOST}:{SERVER_PORT}/fibonacci', params={'n': 10})


if __name__ == '__main__':
    time_start = time.time()

    socket_client()
    # request_client()

    time_finish = time.time()

    print(f'RPS: {num_of_iter / (time_finish - time_start)}')

