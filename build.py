#!/usr/bin/env python3

# _*_coding: UTF-8
import os, sys, base64


def executable(prog):
	cmd = 'pyinstaller -F --onefile /home/acquila/Documentos/Documentos/UFG/7P/SAS/ransomware/cryingariver/{}.py - n {}'.format(prog, prog)
	os.system(cmd)

def encodeFile(prog):
	output = b''
	try:
		with open('dist/{}'.format(prog), 'rb') as file:
			r = file.read()
			output = base64.b64encode(r)
	except:
		print("Can't open {} binary".format(prog))

	with open('dist/base64{}'.format(prog), 'wb') as file:
		file.write(output)

	return output

def build(prog):
	print (prog)
	executable(prog)
	out = encodeFile(prog)
	return out

def main():
	decryptor = build('decryptor')
	daemon = build('daemon')
	
	print ("Decryptor:\n {}".format(decryptor))
	print ("Daemon:\n {}".format(daemon))

if __name__ == '__main__':
	main()

