import base64
from hashlib import md5

from Crypto.Cipher import AES
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms

'''
encrypt_md5 加密
AES/CBC/PKCS7Padding 加密
环境需求:
pip3 install pycryptodome
'''


def encrypt_md5(str_data):
    # 创建md5对象
    new_md5 = md5()
    # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(str_data.encode(encoding='utf-8'))
    # 加密
    return new_md5.hexdigest()


class AesCrypt(object):

    def __init__(self, key='0000000000000000', iv='0000000000000000'):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
        self.iv = iv.encode('utf-8')
        # block_size 128位

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16但是不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        text = text.encode('utf-8')

        # 这里密钥key 长度必须为16（AES-128）,24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用

        text = self.pkcs7_padding(text)

        cipher_text = cryptor.encrypt(text)

        return base64.b64encode(cipher_text)

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()

        padded_data = padder.update(data) + padder.finalize()

        return padded_data


def encrypt_AES(timestamps, pwd):
    md5_str = encrypt_md5('{}{}'.format(timestamps, 'fd#O@7Ej0.U4P2^i'))
    key = md5_str[:16]
    iv = md5_str[16:]
    pc = AesCrypt(key, iv)  # 初始化密钥
    en_pwd = pc.encrypt(pwd).decode()
    return en_pwd


# 加密(系统加密后：QIZ2JGAE7o3jEOtuQzutqw==)
if __name__ == '__main__':
    encrypt_str = encrypt_AES('1615877310430', 'zsy@1221')
    print(encrypt_str)
