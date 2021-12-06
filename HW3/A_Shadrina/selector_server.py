# -*- coding: utf-8 -*-
import socket
from select import select
from typing import Callable

from client import SERVER_HOST, SERVER_PORT
from get_fibonacci import get_fibonacci_value


def get_server_socket() -> socket.socket:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM -> Установка TCP-соединения
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind((SERVER_HOST, SERVER_PORT))
    server_sock.listen()

    return server_sock


to_monitor = []


def accept_connection(server_sock):
    print('Waiting new connection...')
    client_sock, client_addr = server_sock.accept()
    print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    to_monitor.append(client_sock)


def echo(client_sock):
    data = client_sock.recv(4096)
    print(f'Received: {data}')

    if data:
        i = int.from_bytes(data, byteorder='little')
        client_sock.send(i.to_bytes(4, 'little'))
    else:
        print('Client has gone')
        to_monitor.remove(client_sock)
        client_sock.close()


def fibonacci(client_sock):
    data = client_sock.recv(4096)
    print(f'Received: {data}')

    if data:
        n = int.from_bytes(data, byteorder='little')
        f_value = get_fibonacci_value(n)
        client_sock.send(f_value.to_bytes(4, byteorder='big'))
    else:
        print('Client has gone')
        client_sock.close()


def event_loop(task: Callable):
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])
        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                task(sock)


if __name__ == '__main__':
    server_socket = get_server_socket()
    to_monitor.append(server_socket)
    # event_loop(echo)
    event_loop(fibonacci)
