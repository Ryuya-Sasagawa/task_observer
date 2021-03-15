import sys
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


def create_aes(password, iv):
    sha = SHA256.new()
    sha.update(password.encode())
    key = sha.digest()
    return AES.new(key, AES.MODE_CFB, iv)

def encrypt(data, password):
    iv = Random.new().read(AES.block_size)
    return iv + create_aes(password, iv).encrypt(data)

def decrypt(data, password):
    iv, cipher = data[:AES.block_size], data[AES.block_size:]
    return create_aes(password, iv).decrypt(cipher)

def read(path, password):
    with open(path, mode='rb') as f:
        text = f.read()
        dec = decrypt(text, password)
        return dec.decode()

def write(path, password, data):
    with open(path, mode='wb') as f:
        dec = encrypt(data.encode(), password)
        f.write(dec)

if __name__ == '__main__':
    password = 'testtesttest'
    t = read('../data/applicationLog', password)
    print(t)
    # write('data/aesTest6', password, 'aiueoあいうえおアイウエオAIUEO12345')



