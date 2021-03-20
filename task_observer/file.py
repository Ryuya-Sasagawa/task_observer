import sys
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


# passwordから鍵を生成
def create_aes(password, iv):
    sha = SHA256.new()
    sha.update(password.encode())
    key = sha.digest()
    return AES.new(key, AES.MODE_CFB, iv)

# dataをpasswordで暗号化
def encrypt(data, password):
    iv = Random.new().read(AES.block_size)
    return iv + create_aes(password, iv).encrypt(data)

# dataをpasswordで複合
def decrypt(data, password):
    iv, cipher = data[:AES.block_size], data[AES.block_size:]
    return create_aes(password, iv).decrypt(cipher)

# pathで指定されたファイルをpasswordで複合しstrを返す
def read(path, password):
    with open(path, mode='rb') as f:
        text = f.read()
        dec = decrypt(text, password)
        return dec.decode()

# data(str)を、pathで指定されたファイルにpasswordで暗号化して書き込む
def write(path, password, data):
    with open(path, mode='wb') as f:
        dec = encrypt(data.encode(), password)
        f.write(dec)

# debug
if __name__ == '__main__':
    password = 'OiC&0~ktz1%i4nUg1ZodLM+XUPf(f|E9ez_vys9p'
    t = read('../data/log_1', password)
    print(t.split('\n'))
    # write('data/aesTest6', password, 'aiueoあいうえおアイウエオAIUEO12345')



