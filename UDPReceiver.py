from UDPReceiverClass import UDPReceiverClass
import sys

def echo(message):
    print message
    sys.exit()

if __name__ == '__main__':
    if len(sys.argv) is not 4:
        echo("Usage -> |executable| |Source IP address| |Destination IP address| |datagram input file|")
        #Read input file
    try:
        file = open(sys.argv[3], 'rb')
    except IOError:
        echo("Could not open input file.")

    contents = file.read()
    file.close()

    R = UDPReceiverClass(contents, sys.argv[1], sys.argv[2])
    error = R.checkUDP()

    if error == -1:
        usage("Error detected in message!")
    print R
