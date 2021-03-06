"""
The Hong Kong University of Science and Technology
COMP4621 Project 2

This file defines the reliable data transfer protocol
The implementation is basically a Go-Back-N sender. See lecture note # 3 on page 48 for details
"""

import threading

import udt

# implement rdt protocol in send(), right now it just use udt.send --> not reliable

seq_num = 0  # Current sequence number
total_num = 0  # Total # of packets
base = 0  # Base of the sending window
sdr_win = 16  # Default window length
timeout = 0.1  # Default timeout
pkt_buffer = []  # Packets-to-send

'''|-----------------------------|'''
'''| Initialize some mutex locks |'''
'''|                             |'''
'''|         Fill in here        |'''
'''|                             |'''
'''|------------ End ------------|'''

timer = None


class SndThread(threading.Thread):
    """
    Sending thread
    """

    def __init__(self, socket, rcv_addr):
        """
        The constructor of SndThread
        :param socket: Socket that packets are sent to
        :param rcv_addr: Receiver's address
        """
        super().__init__()
        self.sock = socket
        self.rcv_addr = rcv_addr

    def run(self):
        """
        This method defines the task of this thread. Called by thread.start()
        """
        global seq_num
        global timer
        global pkt_buffer

        '''Sending packets until all the packets are ACKed'''
        while True:

            '''Before sending, check whether there is unsent packet in the buffer'''
            if send_condition():

                '''Send the next packet'''
                udt.send(self.sock, self.rcv_addr, pkt_buffer[seq_num])

                '''|----------------------------------------------|'''
                '''| When base equals to seq_num, start the timer |'''
                '''|                                              |'''
                '''|                 Fill in here                 |'''
                '''|                                              |'''
                '''|-------------------- End ---------------------|'''

                '''Increment the sequence number by one'''
                seq_num += 1

                '''Check whether all packets are ACKed'''
            elif end_condition():
                break


class RcvThread(threading.Thread):
    """Receiving thread"""

    def __init__(self, socket, rcv_addr):
        """
        The constructor of RcvThread
        :param socket: The socket that packets are sent to
        :param rcv_addr: The receiver's address
        """
        super().__init__()
        self.sock = socket
        self.rcv_addr = rcv_addr

    def run(self):
        """
        This method defines the task of this thread. Called by thread.start()
        """
        global base
        global timer

        '''Receiving ACKs until all the packets are ACKed'''
        while True:

            '''Receive a packet from udt'''
            pkt, _ = udt.recv(self.sock)

            '''Check whether the ACK is corrupted'''
            if pkt.chk_sum == pkt.compute_checksum():

                '''|--------------------------------------------------------------------|'''
                '''| Update the base of the sender window according to received seq_num |'''
                '''|                                                                    |'''
                '''|                             Fill in here                           |'''
                '''|                                                                    |'''
                '''|--------------------------------- End ------------------------------|'''

                '''|-----------------------------------------------------------|'''
                '''|                       Stop the timer                      |'''
                '''|                                                           |'''
                '''|                        Fill in here                       |'''
                '''|                                                           |'''
                '''|---------------------------- End --------------------------|'''

                '''|-----------------------------------------------------------|'''
                '''|    Start the timer if base doesn't equal to seq_number    |'''
                '''|                                                           |'''
                '''|                        Fill in here                       |'''
                '''|                                                           |'''
                '''|---------------------------- End --------------------------|'''

            else:
                print('Corrupted ACK detected! ACK #', pkt.ack_num)

            '''If all the packets are ACKed, return'''
            if end_condition():
                break


def resend(sock, rcv_addr):
    """
    The task of the resend thread
    :param sock: The socket that packets are sent to
    :param rcv_addr: The receiver's address
    """

    if end_condition():
        return

    print('WARNING: Time out for ACK,', base)
    global timer

    '''|-------------------|'''
    '''| Restart the timer |'''
    '''|                   |'''
    '''|   Fill in here    |'''
    '''|                   |'''
    '''|------- End -------|'''

    '''Resend the packets that are sent earlier but not ACKed'''
    for i in range(base, seq_num):
        udt.send(sock, rcv_addr, pkt_buffer[i])


def end_condition():
    """
    Check whether all the packets are ACKed
    :return: A boolean variable indicating whether all the packets are ACKed
    """

    flag = False

    '''|-------------------------------------------------------|'''
    '''| Check whether all the packets in the buffer are ACKed |'''
    '''|                                                       |'''
    '''|                     Fill in here                      |'''
    '''|                                                       |'''
    '''|----------------------- End ---------------------------|'''

    return flag


def send_condition():
    """
    Check whether there is unsent packet in the buffer
    :return: A boolean variable indicating whether rdt can send the next packet in the buffer
    """

    flag = False

    '''|-----------------------------------------------------------------|'''
    '''| Check whether the sender can send the next packet in the buffer |'''
    '''|                                                                 |'''
    '''|                         Fill in here                            |'''
    '''|                                                                 |'''
    '''|----------------------------- End -------------------------------|'''

    return flag


def set_config(config):
    """
    Setting the configuration for the rdt protocol
    :param config: The configuration
    """
    global timeout
    global sdr_win
    keys = config.keys()
    for key in keys:
        if key == 'timeout':
            timeout = config[key]
        if key == 'win_len':
            sdr_win = config[key]


def send(sock, rcv_addr):
    """
    Sending packets using rdt
    :param sock: Sending packet to the socket
    :param rcv_addr: The receiver's address
    """
    global total_num
    total_num = len(pkt_buffer)
    print('Total # packet: ', total_num)

    '''Leveraging two threads, one for sending and the other one for receiving'''
    snd_thread = SndThread(sock, rcv_addr)
    rcv_thread = RcvThread(sock, rcv_addr)
    snd_thread.start()
    rcv_thread.start()

    '''|-------------------------------------------------------|'''
    '''| Wait for the termination of snd_thread and rcv_thread |'''
    '''|                                                       |'''
    '''|                    Fill in here                       |'''
    '''|                                                       |'''
    '''|----------------------- End ---------------------------|'''

