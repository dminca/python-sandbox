#!/usr/bin/env python2
# NETCAT REPLACEMENT

import getopt
import socket
import subprocess
import sys
import threading

# define global vars
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print "NETCAT Net Tool\n", \
        "", \
        "\tUsage: netcat.py -t target_host -p port\n", \
        "\t-l --listen        - listen on [host]:[port] for\n", \
        "\ticoming connections\n", \
        "\t-e --execute=file_to_run - execute the given file upon\n", \
        "\treceiving a connection\n", \
        "\t-c --command       - initialize a command shell\n", \
        "\t-u --upload=destination    - upon receiving connection upload\n", \
        "\ta file and write to [destination]\n", \
        "", \
        "\tExamples: \n", \
        "\tnetcat.py -t 192.168.0.1 -p 5555 -l -c\n", \
        "\tnetcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe\n", \
        "\tnetcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"\n", \
        "\techo 'ABCDEFGHI' | ./netcat.py -t 192.168.0.1 -p 135\n"
    sys.exit(0)


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read cmdline opts
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"


# listen or just send data from stdin?
if not listen and len(target) and port > 0:
    # read in buffer from cmdline
    # this will block, so send CTRL-D if not sending input
    # to stdin
    buffer = sys.stdin.read()

    # send data off
    client_sender(buffer)



def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to target host
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:

            # wait for data back
            recv_len = 1
            response = ""

            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print response,

            # wait for more input
            buffer = raw_input("")
            buffer += "\n"

            # send it off
            client.send(buffer)

    except:

        print "[*] Exception! Exiting."

        # tear down connection
        client.close()


def server_loop():
    global target

    # if no target defined, listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # spin off thread to handle new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):
    # trim newline
    command = command.rstrip()

    # run cmd and get output
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"

    # send output back to client
    return output


def client_handler(client_socket):
    global upload
    global execute
    global comand

    # check for upload
    if len(upload_destination):
        # read in all of the bytes and write to destination
        file_buffer = ""

        # keep reading data until none is available
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # take these bytes and write them out
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # ack that we wrote file out
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    # check for cmd execution
    if len(execute):
        # run cmd
        output = run_command(execute)

        client_socket.send(output)

    # go in another loop if cmd shell requested
    if command:

        while True:
            # show simple prompt
            client_socket.send("<NETCAT:#> ")

            # receive until linefeed (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # send back cmd output
            response = run_command(cmd_buffer)

            # send back response
            client_socket.send(response)


main()
