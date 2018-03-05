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
  print(" > Locating top secret json information")
  #break the file name to two parts, the name and extension
  fName, fExt = os.path.splitext(os.path.basename(filepath))
  jread = open(fName + ".json", 'r')
  jsonStuff = json.load(jread)
  jread.close()

  filename = jsonStuff['fileName'] + jsonStuff['ext']
  if filename == fName + fExt:
    print(" > top secret json information location")
    print(" > opening " + filepath)
    f = open(filename, 'rb')
    #store the read byte into data
    data = f.read()
    f.close()

    key = b64decode(jsonStuff["key"])
    iv = b64decode(jsonStuff["iv"])

    print(" > Decrypting " + filepath)
    pt = Mydecrypt(data, key, iv)

    print(" > Writing plaintext to file")    
    #convert it back from a byte and make it into a image
    f = open(filename, 'wb')
    f.write(pt)
    f.close()

    print(" > Encryption process complete")

    return pt, fExt
  else:
    print("File does not exist, or it wasn't our fault that this file was corrupted because we did not touch it")
