import binascii, re

def dataBlocks(binary_input):
    return (binary_input[0+i:16+i] for i in range(0, len(binary_input), 16))

def xor(input_value, key):
    return '{0:b}'.format(int(input_value,2) ^ int(key,2))

def DESdecryption(enc_data, key):
    input_data = dataBlocks(enc_data)
    decrypted_data = ''

    for blocks in input_data:

        left_half = blocks[0:8]
        right_half = blocks[8:16]
        check = (xor(right_half, key).zfill(len(right_half)))

        if check == '00000000':
            d = left_half
        else:
            d = ''.join([(xor(right_half, key).zfill(len(right_half))), left_half])

        decrypted_data += d
    return decrypted_data

def desFinalDec(Encdata, no_levels, keys):
    temp = Encdata
    for i in range(no_levels-1,-1,-1):
        Decrypted_data = DESdecryption(temp, keys[i])
        temp = Decrypted_data
    return temp

if __name__ == "__main__":
    data = open('RetreivedEncryptedData','r')
    Encrypted_data = data.read()

    with open('keys') as f:
        content = f.readlines()
    keys = [None]*len(content)
    for i in range(len(content)):
        key = re.findall(r"'(.*?)'",content[i])
        keys[i] = key[0]

    levels = len(keys)

    n = int(bin(int(desFinalDec(Encrypted_data, levels, keys), 2)),2)
    dec_data = binascii.unhexlify('%x' % n)

    text_file = open("DecryptedFile.txt", "w")
    text_file.write(dec_data)
    text_file.close()


