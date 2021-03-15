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

if __name__ == '__main__':
    password = 'testtesttest'
    # with open('data/applicationLog', mode='rb') as f:
    #     text = f.read()
    #     enc = encrypt(text, password)
    #     with open('data/aesTest', mode='wb') as F:
    #         F.write(enc)

    with open('data/aesTest4', mode='rb') as f:
        text = f.read()
        dec = decrypt(text, password)
        with open('data/revTest', mode='wb') as F:
            F.write(dec)
    # TODO: ・監視結果はある程度バッファにためておき、一定に達するかアプリを開いたときに、複合→追記→暗号をする
    #   ・とりあえずは前者のみで、実行中のpythonに外部(タスクチェッカーアプリ)が指示を出せる場合は後者を実装
    #   ・applicationLogの更新時はファイルをロックする。
    #   ・アプリでapplicationLogを使うときは、暗号化したままコピーし、それを復号して使う(追記と重ならないようにするため)。
    #   ・又は、全部をStringに格納する。ただ、データサイズが増えることを考えるとなるべく避けたい。
    #   INFO: AESは10MBのファイルサイズでも0.12秒で暗号、復号化可能
