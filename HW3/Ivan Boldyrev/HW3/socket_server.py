import socket


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


server_socket = get_server_socket()


def request_response():
    while True:
        print('Waiting new connection...')
        client_socket, client_addr = server_socket.accept()
        print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')

        while True:
            request = client_socket.recv(4096)
            print(f'Received: {request}')

            if request:
                print('Sending 10 to client...')
                client_socket.send((10).to_bytes(4, 'big'))
            else:
                print('Client has gone. Closing client socket...')
                client_socket.close()
                break


def cpu_bounds():
    while True:
        print('Waiting new connection...')
        client_socket, client_addr = server_socket.accept()
        print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')

        while True:
            request = client_socket.recv(4096)
            print(f'Received: {request}')

            if request:
                n = int.from_bytes(request, "big")
                fac = factorial(n)
                print(f'Sending {fac} to client...')

                client_socket.send(fac.to_bytes(4, 'big'))
            else:
                print('Client has gone. Closing client socket...')
                client_socket.close()
                break


request_response()
