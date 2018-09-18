from UDPSenderClass import UDPSenderClass

class UDPReceiverClass(UDPSenderClass):

    def __init__(self, i, sourceip, destip):
        UDPSenderClass.__init__(self, i, sourceip, destip)

    #Get header information from sender class
    def getUDPHeader(self):
        self.sourcePort = ord(self.data[0])*256 + ord(self.data[1])
        self.destPort = ord(self.data[2])*256 + ord(self.data[3])
        self.UDPLength = ord(self.data[5])*256 + ord(self.data[4])
        self.dataLength = self.dataLength - 8
        temp = ord(self.data[6])*256 + ord(self.data[7])
        return temp

    #Changes the endian so the checksum can be calculated
    def swapEndian(self):
        self.data = self.data[8:]
        for i in xrange(0, self.dataLength, 2):
            self.data[i], self.data[i+1] = self.data[i+1], self.data[i]

    #Parent function.Inherits from sender
    def checkUDP(self):
        tempCS = self.getUDPHeader()
        self.swapEndian()
        self.addPseudoHeader()
        self.addUDPHeader()
        self.makeBinary()
        self.convertStrings()
        self.checkSum()
        if not tempCS == self.checksum:
            return -1
        self.conIPs()
        del self.binData[0:9]
        self.writeFile('RetreivedEncryptedData')

    def __str__(self):
        return "\nDatagram from \nSource IP address: " + self.csIP + "\nSource-port: "+ str(self.sourcePort) + "\nDest IP address: " + self.cdIP + "\nDest-port: " + str(self.destPort) + "\nLength of data: " + str(self.UDPLength) + "Bytes"
