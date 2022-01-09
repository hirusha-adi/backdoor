import argparse


def main():
    parser = argparse.ArgumentParser(add_help=True)

    # parser.add_argument('-h', '--help', dest="help",
    # default=False, action="store_true", help="Help Manual")

    parser.add_argument('-v', '--verbose', dest="verbose",
                        default=False, action="store_true", help="Verbosity")

    parser.add_argument('-a', '--address', dest="address",
                        default="", type=str, help="Address to Bind to")

    parser.add_argument('-p', '--port', dest="port",
                        default=0, type=int, help="Port to Bind to")

    parser = parser.parse_args()
    print(parser)


main()
