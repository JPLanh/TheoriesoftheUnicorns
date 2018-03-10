import os
import glob
import json
import constant
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def Mydecrypt(cipherText, key, iv):
    #returns a default backend object
    backend = default_backend()

    #method to use all the keys to cipher them, the first to parameters uses the hazmat's libraries 
    #to implement AES and CBC using our key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    
    #enables decryption
    decryptor = cipher.decryptor()

    #returns an unpadding instance because since we padded in encryption we must unpad
    unpadder = padding.PKCS7(constant.PADDING_BLOCK_SIZE).unpadder()w

    #pt (plaintext) is set to the decrypted cipher and  updated until everything is fed into context
    #and then finalized so that this object can no longer be used
    pt = decryptor.update(cipherText)  + decryptor.finalize()
    
    #pt (plaintext) is unpadded and updated and finalized so that this object can no longer be used
    pt = unpadder.update(pt) + unpadder.finalize()

    #announce completion of decryption and return pt
    print(" > Decrypting complete")
    return pt
  
def MyfileDecrypt(filepath):
  print(" > Locating magical unicorns")
  #break the file name to two parts, the name and extension

  #check if file exists
  #if yes, read the file, load the JSon content and close the file
  if os.path.isfile(filepath + ".unicorn"):
    print(" > magical unicorn found")
    jread = open(filepath + ".unicorn", 'r')
    jsonStuff = json.load(jread)
    jread.close()
    
    #separate JSon data into their respective variables
    data = b64decode(jsonStuff["cipher"])
    key = b64decode(jsonStuff["key"])
    iv = b64decode(jsonStuff["iv"])

    #announce decryptionn
    print(" > Decrypting " + filepath)
    #run mydecrypt with JSon variables and get pt
    pt = Mydecrypt(data, key, iv)

    print(" > Managing all files")
    
    #convert it back from a byte and make it into a image
    f = open(filepath + jsonStuff["ext"], 'wb')
    f.write(pt)
    f.close()
    os.remove(filepath + ".unicorn")

    #announce completion of encryption and return pt and variable associated with 'ext'
    print(" > Encryption process complete")
    return pt, jsonStuff["ext"]
  
  #else if file does not exist
  else:
    print("File does not exist, or it wasn't our fault that this file was corrupted because we did not touch it")
