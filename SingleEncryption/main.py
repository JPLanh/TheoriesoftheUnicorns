import os
from glob import glob
import encrypt
import decrypt

from Crypto.PublicKey import RSA
from crytography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitves import serialization

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
    
    #init private key
    #public exponent indicates whwat one mathematical property of the key generation will be
    #65537 is widely used because it is prime, large enough to avoid attacks
    #and can be computed quickly on binary coputers
    #key_size determines how many bits the key is
    #backend is set to the default backend to implement RSABackend
    RSA_privatekey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )    
    
    #init RSA public key encryption object using private key
    RSA_publickey = RSA_privatekey.public_key()
    
    #load pem RSA_Publickey_filepath from RSA_publickey
    RSA_Publickey_filepath = RSA_publickey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    #load pem RSA_Privatekey_filepath from RSA_privatekey
    RSA_Privatekey_filepath = RSA_privatekey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKS8,
        encryption_algorithm=serialization.BestAvailableencryption(b'mypassword')
    )
    
    #RSAencrypt
    RSACipher, C, IV, ext = encrypt.MyRSAEncrypt(file, RSA_Publickey_filepath)
    
    #RSAdecrypt
    RSAPlain, C, IV, ext = decrypt.MyRSADecrypt(RSACipher, C, IV, ext, RSA_Privatekey_filepath)
    


  
      