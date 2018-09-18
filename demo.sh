#!/bin/bash
echo "File to be Encrypted : Data"
sleep 2 
echo
echo "Encrypting the data input file"
sleep 2
python DES_Encryption.py
echo
echo "Sending Encrypted data file via UDP Datagram"
sleep 4
python UDPSender.py EncryptedFile 192.168.0.1 192.168.1.2 66 77 datagram
echo
echo "Receive the datagram file via UDP Receiver"
sleep 4
python UDPReceiver.py 192.168.0.1 192.168.1.2 datagram
echo
echo "Decrypting the received data"
sleep 2
python DES_Decryption.py
echo
echo "The File has been decrypted"
echo
echo "Comparing the data.txt file and DecryptedFile"
diff data.txt DecryptedFile.txt
echo
