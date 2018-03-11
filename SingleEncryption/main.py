import os
from glob import glob
import encrypt
import decrypt
import RSAencrypt
import RSAdecrypt

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

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
  
    #RSA
    C, IV, key, ext = encrypt.MyfileEncrypt(file)
    pt, ext = decrypt.MyfileDecrypt(file)
    
    RSA_Publickey_filepath = None
    RSA_Privatekey_filepath = None
    
    #init RSA public key encryption object
    #public_key = private_key.public_key()
      
    #encyption  
    RSACipher, C, IV, ext = RSAencrypt.MyRSAEncrypt(key, C, IV, ext, RSA_Publickey_filepath)
    
    #decryption
    RSAPlain, C, IV, ext = RSAdecrypt.MyRSADecrypt(RSACipher, C, IV, ext, RSA_Privatekey_filepath)

        
              
      
      #first call MyfileEncrypt(filepath) which will return (C, IV, key, ext)
      #C, IV, key, ext = MyfileEncrypt(filepath)
    
      #init RSA public key encryption object
      #load pem publickey from the RSA_publickey_filepath
      #encrpyt key variable ("key") using RSA publickey in OAEP padding mode
      #result will be RSACipher
      #return (RSACipher, C, IV, ext)
    	
      #do inverse:
      #MyRSADecrypt(RSACipher, C, IV, ext, RSA_Privatekey_filepath)
      #which does exactly the inverse of the above 
      #generate the decrypted file using your previous decryption methods
