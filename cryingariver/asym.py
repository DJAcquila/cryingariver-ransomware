#!/usr/bin/env python
# _*_coding: UTF-8
from os import chmod
import os
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA

class Assym:
    def __init__(self):
        self.PrKey_path = ''
        self.PuKey_path = ''
        self.bit_size = 2048
        self.PrKey_PEM = None
        self.PuKey_PEM = None
        self.key = None

    def generate(self):
        self.key = RSA.generate(self.bit_size)
        self.PrKey_PEM = self.key.exportKey('OpenSSH')
        self.PuKey_PEM = self.key.publickey().exportKey('OpenSSH')

    def encrypt(self, data):
        hash_value = PKCS1_OAEP.new(self.key)
        return hash_value.encrypt(data)

    def decrypt(self, data):
        hash_value = PKCS1_OAEP.new(self.key)
        return hash_value.decrypt(data)
    
    def save_key(self, path):
        self.PrKey_path = os.path.join(path, 'priv.key')
        self.PuKey_path = os.path.join(path, 'public.key')
        with open(self.PrKey_path, 'wb') as file:
            # Flag 0600: usuário pode ler e escrever (-rw-------)
            chmod(self.PrKey_path, 0o600)
            file.write(self.PrKey_PEM) 
        with open(self.PuKey_path, 'wb') as file:
            file.write(self.PuKey_PEM)
        
if __name__ == '__main__':
    assym = Assym()
    assym.generate()
    #assym.save_key('/home/acquila/Documentos/Documentos/UFG/7P/SAS/ransomware/Server')
    print("Private Key: {}\n".format(assym.PrKey_PEM))
    print("Public Key: {}".format(assym.PuKey_PEM ))
    