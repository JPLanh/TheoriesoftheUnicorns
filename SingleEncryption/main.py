import os
from glob import glob
import encrypt
import decrypt

from Crypto.PublicKey imort RSA

flag = True;

while(flag):
  
    print("============Encryptor/Decryptor 6882===========")
    print("encrypt [filename] + [.ext]")
    print("decrypt (.unicorn filename)")
    print("quit")
    getInput = input("Command: ")
    
    if len(getInput.split(" ")) == 2:
        cmd,file = getInput.split(" ")
        if cmd == "encrypt":
            encrypt.MyfileEncrypt("./" + file)
        elif cmd == "decrypt":
            decrypt.MyfileDecrypt("./" + file)
        else:
            print("invalid command")
    elif (len(getInput.split(" ")) == 1):
        if getInput == "quit":
            flag = False;
            print("Good bye")
    else:
         print("Invalid command")
    print()
    
    #RSAencrypt
    #init RSA public key encryption object
    RSA_publickey = private_key.public_key()
    
    #load pem publickey from the RSA_publickey_filepath
    RSA_Publickey_filepath = RSA_publickey.public_bytes(
        encoding=serialization.Encoding.PEM
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )   
    
    #?
    #pem.splitlines()[0]

    RSACipher, C, IV, ext = encrypt.MyRSAEncrypt(file, RSA_Publickey_filepath)
    
    
    #RSAPlain, C, IV, ext = decrypt.MyRSAEncrypt(RSACipher, C, IV, ext, RSA_Privatekey_filepath)

  
      