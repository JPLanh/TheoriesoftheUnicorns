import os
import glob
import json
import constant
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import asymmetric
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives import serialization

def Mydecrypt(cipherText, key, iv):
    #returns a default backend object
    backend = default_backend()

    #method to use all the keys to cipher them, the first to parameters uses the hazmat's libraries 
    #to implement AES and CBC using our key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    
    #enables decryption
    decryptor = cipher.decryptor()

    #returns an unpadding instance because since we padded in encryption we must unpad
    unpadder = padding.PKCS7(constant.PADDING_BLOCK_SIZE).unpadder()

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

    jread = open(filepath + ".unicorn")

    
    #separate JSon data into their respective variables
    jsonStuff = json.load(jread)
    jread.close()
    data = b64decode(jsonStuff["cipher"])
    RSACipher = b64decode(jsonStuff["key"])
    IV = b64decode(jsonStuff["iv"])
    ext = jsonStuff["ext"]
    
    RSA_Privatekey_filepath=os.getcwd() + "/private.pem"

    #Decrypt the RSACipher
    pt, ext = MyRSADecrypt(RSACipher, data, IV, ext, RSA_Privatekey_filepath)

    print(" > Managing all files")
    
    #convert it back from a byte and make it into a image
    f = open(filepath + ext, 'wb')
    f.write(pt)
    f.close()
    os.remove(filepath + ".unicorn")
    
    #announce completion of encryption and return pt and variable associated with 'ext'
    print(" > Encryption process complete")
  
  #else if file does not exist
  else:
    print("File does not exist, or it wasn't our fault that this file was corrupted because we did not touch it")


def MyRSADecrypt(RSACipher, C, IV, ext, RSA_Privatekey_filepath):

    #open RSA_Privatekey_filepath with 'read bytes'
    #load private key and read it
    #in our case there is no password for private key
    f=open(RSA_Privatekey_filepath, 'rb')
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend()
    )
    
    #use private key to decrypt the RSACipher using OAEP padding

    key = private_key.decrypt(
         RSACipher,
         asymmetric.padding.OAEP(
             mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
             algorithm=hashes.SHA256(),
             label=None
         )
    )

    #call Mydecrypt using C, key, and IV to finally receive the original file again
    #announce decryptionn
    print(" > Decrypting filepath")
    pt = Mydecrypt(C, key, IV)
    
    return pt, ext
