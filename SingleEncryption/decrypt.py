import os
import glob
import json
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def Mydecrypt(cipherText, key, iv):
    backend = default_backend()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

    
    #for the decryption part
    decryptor = cipher.decryptor()
    #as we pad thing we have to unpad them
    unpadder = padding.PKCS7(128).unpadder()

    pt = decryptor.update(cipherText)  + decryptor.finalize()
    pt = unpadder.update(pt) + unpadder.finalize()

    print(" > Decrypting complete")
    return pt
  
def MyfileDecrypt(filepath):
  print(" > Locating magical unicorns")
  #break the file name to two parts, the name and extension

  if os.path.isfile(filepath + ".unicorn"):
    print(" > magical unicorn found")
    jread = open(filepath + ".unicorn", 'r')
    jsonStuff = json.load(jread)
    jread.close()

    data = b64decode(jsonStuff["cipher"])
    key = b64decode(jsonStuff["key"])
    iv = b64decode(jsonStuff["iv"])

    print(" > Decrypting " + filepath)
    pt = Mydecrypt(data, key, iv)

    print(" > Managing all files")
    
    #convert it back from a byte and make it into a image
    f = open(filepath + jsonStuff["ext"], 'wb')
    f.write(pt)
    f.close()
    os.remove(filepath + ".unicorn")

    print(" > Encryption process complete")

    return pt, jsonStuff["ext"]
  else:
    print("File does not exist, or it wasn't our fault that this file was corrupted because we did not touch it")
