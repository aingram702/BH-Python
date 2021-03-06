import sys
import socket
import getopt
import threading
import subprocess

# define the global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print("--------------PyCat--The-NetCat-Alternative-----------------")
    print("------------------------------------------------------------")
    print("Usage: pycat.py -t <target_host> -p <port>")
    print("-l --listen              - listen on [host]:[port] for incoming connections")
    print("-e --execute             - execute the given file upon receiving connection")
    print("-c --command             - initialize a command shell")
    print("-u --upload=destination  - upon receiving connection upload a file and write to [destination]")
    print()
    print()
    print("Examples: ")
    print("pycat.py -t 192.168.0.1 -p 5555 -l -c")
    print("pycat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("pycat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./pycat.py -t 192.168.0.1 -p 135")
    sys.exit(0)

def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to target host
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)

        while True:
            # now wait for data
            recv_len = 1
            response = ''

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print(response,)
             # wait for more input
             buffer = raw_input("")
             buffer == "\n"

             # send it off
             client.send(buffer)

    except:
        print("[*] Exception! Exiting.")

        # tear down connection
        client.close()
        

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"

    # are we going to listen or just send data from stdin?
    if not listen and len(target) and port > 0:

        # read in the buffer from the commandline
        # this will block, so send CTRL-D if not sending input to stdin
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer)

    # we are going to listen and potentially upload things, execute commands,
    # and drop a shell depending on our CLI options
    if listen:
        server_loop()


main()