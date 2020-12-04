"""
The Hong Kong University of Science and Technology
COMP4621 Project 2

This file defines the sender
"""

import getopt
import socket
import sys

import rdt
from packet import Packet

# 3 jobs
# read data from file to send
# segment data into packets and store the packets into a packet buffer
# use rdt send to send the packets

def collect_pkt(name, payload_len=512):
    """
    Read data from file-to-send and store the packets into a buffer
    :param name: File name
    :param payload_len: Length of payload in each packet
    :return: Packet buffer
    """
    seq_num = 0
    buffer = []
    try:
        file = open(name, 'rb')
        with file:
            while True:
                chunk = file.read(payload_len)
                if not chunk:
                    break
                buffer.append(Packet(chunk, seq_num))
                seq_num += 1
    except IOError:
        print('File does not exist', name)
        return
    return buffer


def parse_args(argv):
    global file_name
    global ip_addr
    global port
    global rdt_config
    global payload_len

    hlp_msg = 'sender.py -f <file name> -i <receiver ip address> -p <receiver port number> -t <timeout> -w <sender ' \
              'window length> -p <packet payload length> '
    try:
        opts, args = getopt.getopt(argv, "hf:i:p:t:w:l:",
                                   ["file_name=", "ip_addr=", "port_num=", "timeout=", "win_len=", "payload_len"])
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
            port = int(arg)
        elif opt in ('-t', '--timeout'):
            rdt_config['timeout'] = float(arg)
        elif opt in ('-w', '--win_len'):
            rdt_config['win_len'] = int(arg)
        elif opt in ('-p', '--payload_len'):
            payload_len = int(arg)


rdt_config = {'timeout': 0.5, 'win_len': 16}  # The default RDT configuration
payload_len = 512  # The length of payload in a packet
ip_addr = 'localhost'  # Receiver's default IP address
port = 8080  # Receiver's default port number
file_name = 'doc2.txt'  # File-to-send

if __name__ == '__main__':
# read command line arguments
    parse_args(sys.argv[1:])

# Create udp socket
    snd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    snd_socket.bind(('localhost', 0))

    '''Configure the RDT module'''
    rdt.set_config(rdt_config)
    rdt.pkt_buffer = collect_pkt(file_name, payload_len=payload_len)

    '''Send data using RDT'''
    rdt.send(snd_socket, (ip_addr, port))

    snd_socket.close()
