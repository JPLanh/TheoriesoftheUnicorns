import os
import sys
import encrypt
import decrypt
import json
from base64 import b64encode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

flag = True;

while(flag):
  
    print("============Encryptor/Decryptor 6882===========")
    print("encrypt [filename] + [.ext]")
    print("decrypt (.unicorn filename)")
    print("create unicorn")
    print("quit")
    getInput = input("Command: ")
    
    if len(getInput.split(" ")) == 2:
        cmd,file = getInput.split(" ")
        if cmd == "encrypt":            
            RSA_Privatekey_filepath=os.getcwd() + "/public.pem"
            RSACipher, C, IV, ext = encrypt.MyRSAEncrypt(file, RSA_Privatekey_filepath)
            fName = os.path.splitext(os.path.basename(file))
            
            print(" > Managing files")
            #Remove the initial file
            os.remove(file)

            print(" > Generating top secret sensative magical unicorn")
            #create a file with our custom extension so we can write into it
            f = open((fName[0] + ".unicorn"), 'w')

            #dictionary that will be put into the json and into the fake file, unfortunately we can't put byte into json
            #so we have to decode them (convert them to a non-byte)
            topSecretStuff = {}
            topSecretStuff["key"] = b64encode(RSACipher).decode('utf-8')
            topSecretStuff["iv"] = b64encode(IV).decode('utf-8')
            topSecretStuff["cipher"] = b64encode(C).decode('utf-8')
            topSecretStuff["ext"] = ext

            #put everything from the json into the file
            json.dump(topSecretStuff, f)
            #Close.... the json 
            f.close()

        elif cmd == "decrypt":
            decrypt.MyfileDecrypt("./" + file)
        elif cmd == "create":

            
            print(" > Searching for key to the lands of the unicorn")
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )

            print(" > Key has been found, imagining it into existance (generating private.pem file)")
            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
                )

            f=open("private.pem", 'wb')
            f.write(pem)
            f.close()

            print(" > Creating the physical form of the key (public .pem)")
            public_key = private_key.public_key()
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            f=open("public.pem", 'wb')
            f.write(pem)
            f.close()
            
            print(" > Now go find some unicorns")
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
