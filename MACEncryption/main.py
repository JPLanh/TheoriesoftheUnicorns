import os
import sys
import encrypt
import decrypt
import json
import constant
from base64 import b64encode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def generateKey():
    try:
        #try to load open a private key
        private_key = open(constant.PRIVATE_PEM, "rb")
    except:
        print("Unable to find any pair of unicorns")
        #public exponent 65537 is the largest known prime number making it large enought to avoid attacks
        #key size is set to 2048 bits
        #backend implements RSABackend
        print(" > Searching for key to the lands of the unicorn")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        #serialize the key
        print(" > Key has been found, imagining it into existance (generating private.pem file)")
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
            )
        #open private.pem key using 'write bytes' and write it
        #close key file
        f=open(constant.PRIVATE_PEM, 'wb')
        f.write(pem)
        f.close()
            
        print(" > Creating the physical form of the key (public .pem)")
        public_key = private_key.public_key()
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        #open public.pem key using 'write bytes' and write
        #close public key file
        f=open(constant.PUBLIC_PEM, 'wb')
        f.write(pem)
        f.close()
            
    try:
        public_key = open(constant.PUBLIC_PEM, "rb")
    except:
        #if a private key exist without a public key
        private_key_load = serialization.load_pem_private_key(
            private_key.read(),
            password=None,
            backend=default_backend()
        )
        print("Current private unicorn does not have any mate :C, lets go find one")
        print(" > Creating the physical form of the key (public .pem)")
        public_key = private_key_load.public_key()
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        #open public.pem key using 'write bytes' and write
        #close public key file
        f=open(constant.PUBLIC_PEM, 'wb')
        f.write(pem)
        f.close()
           
    print(" > Now go find some unicorns")

def encryptionProcess(fileName):
    RSA_Publickey_filepath=os.getcwd() + "/" + constant.PUBLIC_PEM
    RSACipher, C, IV, tag, ext = encrypt.MyRSAEncryptMAC(fileName, RSA_Publickey_filepath)
    fName = os.path.splitext(os.path.basename(fileName))
    
    print(" > Managing files")
    #Remove the initial file
    os.remove(fileName)

    print(" > Generating top secret sensative magical unicorn")
    #create a file with our custom extension so we can write into it
    f = open((fName[0] + ".unicorn"), 'w')

    #dictionary that will be put into the json and into the fake file, unfortunately we can't put byte into json
    #so we have to decode them (convert them to a non-byte)
    topSecretStuff = {}
    topSecretStuff["key"] = b64encode(RSACipher).decode('utf-8')
    topSecretStuff["iv"] = b64encode(IV).decode('utf-8')
    topSecretStuff["tag"] = b64encode(tag).decode('utf-8')
    topSecretStuff["cipher"] = b64encode(C).decode('utf-8')
    topSecretStuff["ext"] = ext

    #put everything from the json into the file
    json.dump(topSecretStuff, f)
    #Close.... the json 
    f.close()    

flag = True;

while(flag):
  
    print("============Encryptor/Decryptor 6882===========")
    print("encrypt [filename] + [.ext]")
    print("encrypt all")
    print("decrypt (.unicorn filename)")
    print("decrypt all")
    print("create unicorn")
    print("quit")
    getInput = input("Command: ")
    
    if len(getInput.split(" ")) == 2:
        cmd,file = getInput.split(" ")
        if cmd == "encrypt":
            if (file == "all"):
                file_List = os.listdir()
                for x in file_List:
                    if x not in ("constant.py", "encrypt.py", "decrypt.py", "main.py",
                                 constant.PRIVATE_PEM, constant.PUBLIC_PEM):
                        if (not x.endswith('.unicorn')):
                            if (os.path.isfile(x)):
                                encryptionProcess(x)
            else:
                encryptionProcess(file)
        elif cmd == "decrypt":
            if file == "all":
                file_List = os.listdir()
                for x in file_List:
                    if x.endswith('.unicorn'):
                        decrypt.MyfileDecryptMAC("./" + x)
            else:
                decrypt.MyfileDecryptMAC("./" + file +".unicorn")
        elif cmd == "create":
            generateKey()
        else: #if user inputs anything but given commands:
            print("invalid command")
    elif (len(getInput.split(" ")) == 1):
        if getInput == "quit":
            flag = False;
            print("Good bye")
            #sys.exit()
    else:
         print("Invalid command")
    print()
