import socket
from select import select


def factorial(n):
    fac = 1
    while n > 1:
        fac *= n
        n -= 1
    return fac


def get_server_socket():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 8090))
    server_sock.listen()

    return server_sock


to_monitor = []


def accept_connection(server_sock: socket.socket) -> None:
    client_socket, client_addr = server_sock.accept()
    print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    to_monitor.append(client_socket)


def send_message(client_sock: socket.socket) -> None:
    request = client_sock.recv(4096)
    print(f'Received: {request}')

    if request:
        print('Sending 10 to client...')
        client_sock.send((10).to_bytes(4, 'big'))
    else:
        print('Client has gone. Closing client socket...')
        to_monitor.remove(client_sock)
        client_sock.close()


def send_factorial(client_sock: socket.socket):
    request = client_sock.recv(4096)
    print(f'Received: {request}')

    if request:
        n = int.from_bytes(request, "big")
        fac = factorial(n)
        print(f'Sending {fac} to client...')
        client_sock.send(fac.to_bytes(4, 'big'))
    else:
        print('Client has gone. Closing client socket...')
        to_monitor.remove(client_sock)
        client_sock.close()


def event_loop(response_type):
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])
        for sock in ready_to_read:
            if sock == server_socket:
                accept_connection(sock)
            else:
                if response_type == 'mes':
                    send_message(sock)
                if response_type == 'fac':
                    send_factorial(sock)


if __name__ == '__main__':
    server_socket = get_server_socket()
    to_monitor.append(server_socket)
    event_loop('fac')
