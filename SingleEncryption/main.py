import os
#from glob import glob
import sys
import encrypt
import decrypt

#from Crypto.PublicKey import RSA
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
#from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKeyWithSerialization
#from OpenSSL import crypto

#load private key
#ftype=crypto.FILETYPE_PEM
#with open('unicornkey.pem', 'rb') as f: key=f.read()
#key=crypto.load_privatekey(ftype, key)

#init private key
#public exponent indicates whwat one mathematical property of the key generation will be
#65537 is widely used because it is prime, large enough to avoid attacks
#and can be computed quickly on binary coputers
#key_size determines how many bits the key is
#backend is set to the default backend to implement RSABackend
#RSA_privatekey = rsa.generate_private_key(
#    public_exponent=65537,
#    key_size=2048,
#    backend=default_backend()
#)    

#init RSA public key encryption object using private key
#RSA_publickey = RSA_privatekey.public_key()

#load pem RSA_Publickey_filepath from RSA_publickey
#RSA_Publickey_filepath = RSA_publickey.public_bytes(
#    encoding=serialization.Encoding.PEM,
#    format=serialization.PublicFormat.SubjectPublicKeyInfo
#)

#load pem RSA_Privatekey_filepath from RSA_privatekey
#RSA_Privatekey_filepath = RSA_privatekey.private_bytes(
#    encoding=serialization.Encoding.PEM,
#    format=serialization.PrivateFormat.TraditionalOpenSSL,
#    encryption_algorithm=serialization.NoEncryption()
#)

flag = True;

while(flag):
  
    print("============Encryptor/Decryptor 6882===========")
    print("encrypt [filename] + [.ext]")
    print("decrypt (.unicorn filename)")
    print("quit")
    getInput = raw_input("Command: ")
    
    if len(getInput.split(" ")) == 2:
        cmd,file = getInput.split(" ")
        if cmd == "encrypt":
            #encrypt.MyfileEncrypt("./" + file)
            RSA_Publickey_filepath=os.getcwd() + "/unicorn.pub"
            RSACipher, C, IV, ext = encrypt.MyRSAEncrypt(file, RSA_Publickey_filepath)
            print(" > Managing files")
            #Remove the initial file
            os.remove(filename)

            print(" > Generating top secret sensative magical unicorn")
            #create a file with our custom extension so we can write into it
            f = open(fName + ".unicorn", 'w')

            #dictionary that will be put into the json and into the fake file, unfortunately we can't put byte into json
            #so we have to decode them (convert them to a non-byte)
            topSecretStuff = {}
            topSecretStuff["key"] = RSACipher 
            topSecretStuff["iv"] = b64encode(IV).decode('utf-8')
            topSecretStuff["cipher"] = b64encode(ct).decode('utf-8')
            topSecretStuff["ext"] = fExt

            #put everything from the json into the file
            json.dump(topSecretStuff, f)
            #Close.... the json 
            f.close()
        elif cmd == "decrypt":
            decrypt.MyfileDecrypt("./" + file)
        else:
            print("invalid command")
    elif (len(getInput.split(" ")) == 1):
        if getInput == "quit":
            flag = False;
            print("Good bye")
            #sys.exit()
    else:
         print("Invalid command")
    print()
    
    #RSAdecrypt
    #RSAPlain, C, IV, ext = decrypt.MyRSADecrypt(RSACipher, C, IV, ext, RSA_Privatekey_filepath)
    

  
      
