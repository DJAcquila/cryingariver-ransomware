#!/usr/bin/env python3
# _*_coding: UTF-8

import base64, hashlib
from Crypto import Random 
from Crypto.Cipher import AES
from randomkey import generate_randomKey

class AESHash:
	def __init__(self, key):
		# A chave usada para criação da mensagem cifrada será codificada em SHA256
		self.key = hashlib.sha256(key).digest()

	# Ao criptografar a mensagem, a transforma para a base64
	def encrypt(self, msg):
		msg = msg + (32 - len(msg) % 32) * chr(32 - len(msg) % 32)

		IV = Random.new().read(AES.block_size)
		cipher = AES.new(self.key, AES.MODE_CBC, IV)
		return base64.b64encode(IV + cipher.encrypt(msg))

	# Recebe uma mensagem criptografada com AES, convertida para a base64
	def decrypt(self, encrypMsg, decryption_key=None):
		encrypMsg = base64.b64decode(encrypMsg)
		iv = encrypMsg[:AES.block_size]
		if(decryption_key):
			self.key = hashlib.sha256(decryption_key).digest()
			
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		s = cipher.decrypt(encrypMsg[AES.block_size:])
		return s[:-ord(s[len(s)-1:])]


if __name__ == '__main__':
	key = generate_randomKey(32, True)
	cipher_obj = AESHash(key)
	string = 'Teste'

	e = cipher_obj.encrypt(string)
	print(base64.b64decode(e))

	b = cipher_obj.decrypt(e, key)
	print(b)