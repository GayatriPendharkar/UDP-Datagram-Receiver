class UDPSenderClass(object):
    # Constuctor
    def __init__(self, i, sip, dip, sp=0, dp=0, dg=None):
        self.data = list(i)
        self.dataLength = len(self.data)
        self.UDPLength = 0
        self.sourceIP = list(sip.split('.'))
        self.destIP = list(dip.split('.'))
        self.sourcePort = int(sp)
        self.destPort = int(dp)
        self.datagram = dg
        self.binData = []
        self.bdi = 0
        self.checksum = 0
        self.csIP = ''
        self.cdIP = ''

    #Determining length of data and UDP header in bytes
    def setLength(self, header):
        self.UDPLength = self.dataLength + header

    #pads data if its not even
    def addPadding(self):
        if len(self.data) % 2 is 1:
            self.data.append(str(0))

    #Forming the pseudo header
    def addPseudoHeader(self):
        #Add Source IP address
        for i in xrange(0, len(self.sourceIP), 2):
            self.binData.append('{0:08b}'.format(int(self.sourceIP[i])))
            self.binData[self.bdi] += '{0:08b}'.format(int(self.sourceIP[i + 1]))
            self.bdi += 1
        #Add Destination IP address
        for i in xrange(0, len(self.destIP), 2):
            self.binData.append('{0:08b}'.format(int(self.destIP[i])))
            self.binData[self.bdi] += '{0:08b}'.format(int(self.destIP[i + 1]))
            self.bdi += 1

        #Add zeros, protocol value = 17 and UDP length
        self.binData.append('0000000000010001')
        self.binData.append('{0:016b}'.format(self.UDPLength))
        self.bdi += 2

    #Adds source and destination port numbers and length in binary
    def addUDPHeader(self):
        self.binData.append('{0:016b}'.format(self.sourcePort))
        self.binData.append('{0:016b}'.format(self.destPort))
        self.binData.append('{0:016b}'.format(self.UDPLength))
        self.bdi += 3

    #Concatenates binary Data for Checksum calculation
    def makeBinary(self):
        for i in xrange(0, len(self.data), 2):
            self.binData.append('{0:08b}'.format(ord(self.data[i])))
            self.binData[self.bdi] += '{0:08b}'.format(ord(self.data[i + 1]))
            self.bdi += 1

    #Converts Binary back into integers
    def convertStrings(self):
        for i in xrange(0, len(self.binData)):
            self.binData[i] = int(self.binData[i], 2)

    #Computes Checksum
    def checkSum(self):
        self.checksum = self.binData[0]
        for i in xrange(1, len(self.binData)):
            self.checksum += self.binData[i]
            # For carry. Cannot exceed 65535 for 16 bits
            if self.checksum > 65535:
                self.checksum = self.checksum - 65535
        self.checksum = self.checksum ^ 65535

    # Removes pseudoheader and inserts check sum value
    def createDatagram(self):
        for i in xrange(6):
            del self.binData[0]
        for i in xrange(2, len(self.binData)):
            self.binData[i] = self.changeEndian(self.binData[i])
        self.binData.insert(3, self.checksum)

    def changeEndian(self, bEnd):
        value = '{0:016b}'.format(bEnd)
        f, s = value[0:8], value[8:16]
        value = s + f
        return int(value, 2)

    #Writes binary file to output file passed in arguments
    def writeFile(self, fileName):
        file = open(fileName, 'wb')
        for i in xrange(len(self.binData) - 1):
            value = '{0:016b}'.format(self.binData[i])
            file.write(chr(int(value[0:8], 2)))
            file.write(chr(int(value[8:16], 2)))
        if len(self.data) % 2 is 1:
            value = '{0:016b}'.format(self.binData[-1])
            file.write(chr(int(value[0:8], 2)))
        else:
            value = '{0:016b}'.format(self.binData[-1])
            file.write(chr(int(value[0:8], 2)))
            file.write(chr(int(value[8:16], 2)))
        file.close()

    #Converts IP addresses to hex
    def conIPs(self):
        for i in xrange(len(self.sourceIP) - 1, -1, -1):
            temp = format(int(self.sourceIP[i]), '02x')
            self.csIP += temp
            temp = format(int(self.destIP[i]), '02x')
            self.cdIP += temp

    #Parent function. Calls all other functions
    def createUDP(self):
        self.setLength(8)
        self.addPadding()
        self.addPseudoHeader()
        self.addUDPHeader()
        self.makeBinary()
        self.convertStrings()
        self.checkSum()
        self.createDatagram()
        self.writeFile(self.datagram)
        self.conIPs()

    #To string method
    def __str__(self):
        return "\nBig-endian IP:\n\nSource IP: " + self.csIP + "\nDestination IP: " + \
                self.cdIP + "\n\nSource IP byte 1: " + str(self.sourceIP[0]) + "\nSource IP byte 2: " + \
                str(self.sourceIP[1]) + "\nSource IP byte 3: " + str(self.sourceIP[2]) + "\nSource IP byte 4: " + \
                str(self.sourceIP[3]) + "\nDestination IP byte 1: " + str(self.destIP[0]) + "\nDestination IP byte 2: " + \
                str(self.destIP[1]) + "\nDestination IP byte 3: " + str(self.destIP[2]) + "\nDestination IP byte 4: " + \
                str(self.destIP[3]) + "\n\nSource port: " + str(self.sourcePort) + "\nDestination port: " + str(self.destPort) + \
                "\n\nfile size (Byte, without zero padding): " + str(self.dataLength) + "\ntotal length(bytes): " + \
                str(self.UDPLength) + "\n\nChecksum: " + str(hex(self.checksum).lstrip("0x")) + \
                "\n\nFile was successfully written to " + self.datagram + "\n"
