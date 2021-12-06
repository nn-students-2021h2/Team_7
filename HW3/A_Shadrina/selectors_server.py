# -*- coding: utf-8 -*-
import selectors
import socket

from client import SERVER_HOST, SERVER_PORT
from get_fibonacci import get_fibonacci_value

selector = selectors.DefaultSelector()


def run_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM -> Установка TCP-соединения
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind((SERVER_HOST, SERVER_PORT))
    server_sock.listen()

    selector.register(
        fileobj=server_sock,
        events=selectors.EVENT_READ,
        data=accept_connection
    )


def accept_connection(server_sock):
    print('Waiting new connection...')
    client_sock, client_addr = server_sock.accept()
    print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    selector.register(
        fileobj=client_sock,
        events=selectors.EVENT_READ,
        # data=echo
        data=fibonacci
    )


def echo(client_sock):
    data = client_sock.recv(4096)
    print(f'Received: {data}')

    if data:
        i = int.from_bytes(data, byteorder='little')
        client_sock.send(i.to_bytes(4, 'little'))
    else:
        print('Client has gone')
        selector.unregister(client_sock)
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
        selector.unregister(client_sock)
        client_sock.close()


def event_loop():
    while True:
        events = selector.select()  # -> List[Tuple[]]
        for key, _ in events:  # key = fileobj, events, data (Callable)
            callback = key.data  # accept_connection
            callback(key.fileobj)  # accept_connection(server_sock)


if __name__ == '__main__':
    run_server()
    event_loop()
