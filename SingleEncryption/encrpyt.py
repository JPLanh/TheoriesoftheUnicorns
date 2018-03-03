import os
import glob
import json
from base64 import b64encode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def Myencrypt(message, key):
    if (len(key) == 32):
      #not sure about this part
      backend = default_backend()
      #randomize the iv, but not sure if it suppose to be this way because we will need to reuse it for later
      IV = os.urandom(16)
  
      #it's a method to use all the keys to cipher them the first two parameter uses the libraries to implement AES and CBC using our key and IV
      C = Cipher(algorithms.AES(key), modes.CBC(IV), backend=backend)

      return C, IV

def MyfileEncrypt(filepath): 
  #randomize the key, but not sure if it is suppose to be this way because we will need to reuse it for later
  key = os.urandom(32)
  #break the file name to two parts, the name and extension
  fName, fExt = os.path.splitext(os.path.basename(filepath))
  #get the path of the file
  path = os.path.dirname(filepath)

  #reads the file as a byte 
  f = open(filepath, 'rb')
  #store the read byte into data
  data = f.read()
  #always close after an open
  f.close()

  #Run the method to get the cipher and the IV
  C, IV = Myencrypt(data, key)
  
  #initalize the padder because CBC needs a padder
  padder = padding.PKCS7(128).padder()

  #enables our encrpytion
  encryptor = C.encryptor()

  #================== Core of it all
  #This will pad the bytes and then finalize it, as in it will return the rest after the last block is done
  ct = padder.update(data) + padder.finalize()
  #after it has been padded, it will be encrypted.. remember since it's block it need to finish and return the rest
  ct = encryptor.update(ct) + encryptor.finalize()

  #Create the fake file
  filename = path + "\\" + fName + fExt
  print(filename)
  f = open(filename, 'wb')
  #write the encrypted byte into the file
  f.write(ct)
  f.close()

  #create a json so we can write into it
  f = open('topSecretStuff.json', 'w')

  #dictionary that will go into the JSON, unfortunately we can't put byte into json
  #so we have to decode them (convert them to a non-byte)
  topSecretStuff = {}
  topSecretStuff["key"] = b64encode(key).decode('utf-8')
  topSecretStuff["iv"] = b64encode(IV).decode('utf-8')
  topSecretStuff["path"] = path
  topSecretStuff["fileName"] = fName
  topSecretStuff["ext"] = fExt

      
  #put everything from the list into the json
  json.dump(topSecretStuff, f)
  #Close.... the json 
  f.close()

#some hardcoding for now
MyfileEncrypt('.\\test2\\traktor.jpg')