'''

This is the template that should be used for client modules.
A brief description of the client module can/should be placed
up here.  All necessary imports should be placed between the
comments and class declaration.

Finally, be sure to rename your client module to a .py file

'''

import base64
import re
import socket
import sys
from common import helpers
from scapy.all import *


class Client:

    def __init__(self, cli_object):
        self.protocol = "icmp"
        self.length = 1100   # Number of cleartext characters allowed before b64 encoded
        self.remote_server = cli_object.ip

    def transmit(self, data_to_transmit):

        byte_reader = 0
        packet_number = 1

        # Determine if sending via IP or domain name
        if helpers.validate_ip(self.remote_server):
            final_destination = self.remote_server
        else:
            print "[*] Resolving IP of domain..."
            final_destination = socket.gethostbyname(self.remote_server)

        while (byte_reader < len(data_to_transmit) + self.length):
            encoded_data = base64.b64encode(data_to_transmit[byte_reader:byte_reader + self.length])

            # calcalate total packets
            if ((len(data_to_transmit) % self.length) == 0):
                total_packets = len(data_to_transmit) / self.length + 1
            else:
                total_packets = (len(data_to_transmit) / self.length) + 2

            print "[*] Packet Number/Total Packets:        " + str(packet_number) + "/" + str(total_packets)

            # Craft the packet with scapy
            try:
                send(IP(dst=final_destination)/ICMP()/(encoded_data), verbose=False)
            except KeyboardInterrupt:
                print "[*] Shutting down..."
                sys.exit()

            # Increment counters
            byte_reader += self.length
            packet_number += 1

        return
