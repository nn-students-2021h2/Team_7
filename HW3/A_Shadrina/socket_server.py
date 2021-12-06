# -*- coding: utf-8 -*-
import socket

from get_fibonacci import get_fibonacci_value
from client import SERVER_HOST, SERVER_PORT


def get_server_socket() -> socket.socket:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM -> Установка TCP-соединения
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind((SERVER_HOST, SERVER_PORT))
    server_sock.listen()

    return server_sock


server_socket = get_server_socket()


def echo():
    while True:
        print('Waiting new connection...')
        client_socket, client_addr = server_socket.accept()
        print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')

        while True:
            data = client_socket.recv(4096)
            print(f'Received: {data}')

            if data:
                i = int.from_bytes(data, byteorder='little')
                client_socket.send(i.to_bytes(4, 'little'))
            else:
                print('Client has gone')
                client_socket.close()
                break


def fibonacci():
    while True:
        print('Waiting new connection...')
        client_socket, client_addr = server_socket.accept()
        print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')

        while True:
            data = client_socket.recv(4096)
            print(f'Received: {data}')

            if data:
                n = int.from_bytes(data, byteorder='big')
                f_value = get_fibonacci_value(n)
                print(f'Sending response to client...')
                client_socket.send(f_value.to_bytes(4, byteorder='big'))
            else:
                print('Client has gone')
                client_socket.close()
                break


if __name__ == '__main__':
    # echo()
    fibonacci()
