"""This file defines the sender"""

import getopt
import socket
import sys

import rdt


def parse_args(argv):
    """
    Read command line arguments
    :param argv: Command line arguments
    """
    global file_name    # File-to-send
    global ip_addr    # Receiver's IP address
    global port    # Receiver's port number
    global payload_len    # Length of payload in each packet

    hlp_msg = 'sender.py -f <file name> -i <receiver ip address> -p <receiver port number> -p <packet payload length> '
    try:
        opts, args = getopt.getopt(argv, "hf:i:p:l:",
                                   ["file_name=", "ip_addr=", "port_num=", "payload_len"])
    except getopt.GetoptError:
        print(hlp_msg)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(hlp_msg)
            sys.exit()
        elif opt in ("-f", "--file_name"):
            file_name = arg
        elif opt in ("-i", "--ip_addr"):
            ip_addr = arg
        elif opt in ('-p', '--port_num'):
            port = arg
        elif opt in ('-p', '--payload_len'):
            payload_len = arg


file_name = 'doc2.txt'    # File-to-send
payload_len = 512    # Payload length
ip_addr = 'localhost'    # Receiver's ID address
port = 8080    # Receiver's port number

if __name__ == '__main__':
    '''Read command line arguments'''
    parse_args(sys.argv[1:])

    '''Create an UDP socket'''
    snd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    snd_socket.bind(('localhost', 0))
    
    '''Prepare the packet buffer'''
    pkt_buffer = []

    '''Send data to the receiver'''
    with snd_socket:
        rdt.send(snd_socket, (ip_addr, port))
