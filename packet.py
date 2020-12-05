"""
The Hong Kong University of Science and Technology
COMP4621 Project 2

This file defines the packet format
"""


class Packet:
    def __init__(self, payload=b"", seq_num=0, ack_num=0):
        """
        Constructor of class Packet
        :param payload: Data carried in this packet
        :param seq_num: Sequence number of this packet
        :param ack_num: ACK number of this packet
        """
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.payload = payload
        self.chk_sum = 0
        self._init_checksum()

    def encode(self):
        """
        Encode a packet into bytes
        :return: A byte stream
        """
        seq_byte = self.seq_num.to_bytes(4, byteorder='big', signed=True)
        ack_byte = self.ack_num.to_bytes(4, byteorder='big', signed=True)
        chk_byte = self.chk_sum.to_bytes(4, byteorder='big', signed=True)
        return seq_byte + ack_byte + chk_byte + self.payload

    def decode(self, packet):
        """
        Decode a packet from bytes
        :param packet: A packet in bytes
        :return: A Packet object
        """

        '''|-----------------------------------------|'''
        '''| Decode a byte stream to a Packet object |'''
        '''|                                         |'''
        # packets in int
        self.seq_num = int.from_bytes(packet[0:4], byteorder='big', signed=True)
        self.ack_num = int.from_bytes(packet[4:8], byteorder='big', signed=True) 
        self.chk_sum = int.from_bytes(packet[8:12], byteorder='big', signed=True)

        # length = int.from_bytes(packet[12:16], byteorder='big', signed=True)
        # l = 16+length
        self.payload = packet[12:]
        # self.payload = bytes(packet[16:l])
        '''|              Fill in here               |'''
        '''|                                         |'''
        '''|------------------ End ------------------|'''

        return self

    def __str__(self):
        return f"{self.seq_num} {self.ack_num} {self.chk_sum} \n {self.payload.decode()}"

    def _init_checksum(self):
        self.chk_sum = self.compute_checksum()

    def compute_checksum(self):
        """
        Compute the checksum of a packet (Based on internet resources)
        :return: The checksum of this packet
        """
        pkt_byte = self.encode()
        byte_msg = pkt_byte[0:8] + pkt_byte[12:]
        total = 0
        length = len(byte_msg)
        i = 0
        while length > 1:
            total += ((byte_msg[i + 1] << 8) & 0xFF00) + ((byte_msg[i]) & 0xFF)
            i += 2
            length -= 2

        if length > 0:
            total += (byte_msg[i] & 0xFF)

        while (total >> 16) > 0:
            total = (total & 0xFFFF) + (total >> 16)

        total = ~total
        return total & 0xFFFF
