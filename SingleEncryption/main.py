import os
import sys
import encrypt
import decrypt
import json
from base64 import b64encode

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
            RSA_Publickey_filepath=os.getcwd() + "/unicornkey.pem"
            RSACipher, C, IV, ext = encrypt.MyRSAEncrypt(file, RSA_Publickey_filepath)
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
