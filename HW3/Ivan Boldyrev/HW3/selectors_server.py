import selectors
import socket


def factorial(n):
    fac = 1
    while n > 1:
        fac *= n
        n -= 1
    return fac


selector = selectors.DefaultSelector()


def server(response_type):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 8090))
    server_sock.listen()
    if response_type == 'mes':
        selector.register(
            fileobj=server_sock,
            events=selectors.EVENT_READ,
            data=accept_connection
        )
    if response_type == 'fac':
        selector.register(
            fileobj=server_sock,
            events=selectors.EVENT_READ,
            data=accept_fac_connection
        )


to_monitor = []


def accept_connection(server_sock: socket.socket) -> None:
    client_socket, client_addr = server_sock.accept()
    print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
    )


def accept_fac_connection(server_sock: socket.socket) -> None:
    client_socket, client_addr = server_sock.accept()
    print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_factorial
    )


def send_message(client_sock: socket.socket) -> None:
    request = client_sock.recv(4096)
    print(f'Received: {request}')

    if request:
        print('Sending 10 to client...')
        client_sock.send((10).to_bytes(4, 'big'))
    else:
        print('Client has gone. Closing client socket...')
        selector.unregister(client_sock)
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
        selector.unregister(client_sock)
        client_sock.close()


def event_loop():
    while True:
        events = selector.select()  # key, events (bit mask read or write)
        for key, _ in events:  # key has fileobj, events, data
            callback_function = key.data
            callback_function(key.fileobj)


if __name__ == '__main__':
    server('fac')
    event_loop()
