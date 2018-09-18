import sys
import math
from UDPSenderClass import UDPSenderClass

#error function
def echo(message):
    print message
    sys.exit()

#Main Function
if __name__ == '__main__':

    #check number of arguments
    if len(sys.argv) is not 7:
        echo("Usage -> |executable| |encrypted_input file| |source IP address| |destination IP address| |source-port| |destination-port| |datagram file_name|")

    #Read Input File
    try:
        EncFile = open(sys.argv[1], 'rb')
    except IOError:
        echo("Could not open input file.")

    contents = EncFile.read()
    EncFile.close()

    #create an object of the UDPSenderClass
    S = UDPSenderClass(contents, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

    #call parent function of class
    S.createUDP()
    print str(S)
