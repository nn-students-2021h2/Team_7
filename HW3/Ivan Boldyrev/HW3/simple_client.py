import socket
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 8090


client_socket = socket.socket()
client_socket.connect((SERVER_HOST, SERVER_PORT))

start = time.time()
for i in range(1000):
    client_socket.send((10).to_bytes(4, 'big'))
    response = client_socket.recv(100)
    # print(f'{int.from_bytes(response, "big")} was received')
client_socket.close()
stop = time.time()
print('TIME: ', stop-start)
print('RPS: ', 1000/(stop-start))
