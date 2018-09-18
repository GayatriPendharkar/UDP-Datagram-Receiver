import binascii, re

def dataBlocks(binary_input):
    return (binary_input[0+i:16+i] for i in range(0, len(binary_input), 16))

def xor(input_value, key):
    return '{0:b}'.format(int(input_value,2) ^ int(key,2))


def DESencryption(binData, key):
    input_data = dataBlocks(binData)
    encrypted_data = ''

    for blocks in input_data:
        if len(blocks) < 16:
            blocks = blocks.zfill(16)
            left_half = blocks[0:8]
            right_half = blocks[8:16]
        else:
            left_half = blocks[0:8]
            right_half = blocks[8:16]
        e = ''.join([right_half,(xor(left_half, key))])
        encrypted_data += e
    return encrypted_data

def desFinalEnc(BinData, no_levels, keys):
    temp = BinData
    for i in range(no_levels):
        Encrypted_data = DESencryption(temp, keys[i])
        temp = Encrypted_data
    return temp

if __name__ == "__main__":

    data = open('data.txt','r')
    s = data.read()

    with open('keys') as f:
        content = f.readlines()
    keys = [None]*len(content)
    for i in range(len(content)):
        key = re.findall(r"'(.*?)'",content[i])
        keys[i] = key[0]

    levels = len(keys)


    binary_data = bin(int(binascii.hexlify(s), 16))[2:].zfill(len(s)*8)
    #print 'Final Encrypted data is: ', desFinalEnc(binary_data, levels, keys)

    text_file = open("EncryptedFile", "w")
    text_file.write(desFinalEnc(binary_data, levels, keys))
    text_file.close()