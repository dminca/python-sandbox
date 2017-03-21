#!/usr/bin/env python2
# NETCAT REPLACEMENT

import sys
import socket
import getopt
import threading
import subprocess

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


    for o,a in opts:
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

# we listen and upload things, execute cmds, and drop a shell back
# depending on our cmdline opts above
if listen:
    server_loop()

main()

