import os
import glob
import constant
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives import asymmetric
from cryptography.hazmat.primitives import serialization


def Myencrypt(message, key):
    if (len(key) == constant.KEY_BYTE_REQUIREMENT):
      backend = default_backend()
      #Randomize the IV with the specified IV_BYTE
      IV = os.urandom(constant.IV_BYTE)
  
      #method to use all the keys to cipher them, the first two parameter uses the hazmat's libraries to implement AES and CBC using our key and IV
      C = Cipher(algorithms.AES(key), modes.CBC(IV), backend=backend)
        
      #initalize the padder because CBC needs a padder
      padder = padding.PKCS7(constant.PADDING_BLOCK_SIZE).padder()

      #enables our encrpytion
      encryptor = C.encryptor()

      #================== Core of it all
      #This will pad the bytes and then finalize it, as in it will return the rest after the last block is done
      ct = padder.update(message) + padder.finalize()
      #after it has been padded, it will be encrypted.. remember since it's block it need to finish and return the rest
      ct = encryptor.update(ct) + encryptor.finalize()

      print(" > Encryption complete")
      return ct, IV
    else:
      #Intentional mispell for the fun
      raise ValueError('There is a hacker on the loose trying to steal teh code')

def MyfileEncrypt(filepath):

  print(" > Opening " + filepath)
  if (os.path.isfile(filepath)):
      #break the file name to two parts, the name and extension
      fName, fExt = os.path.splitext(os.path.basename(filepath))
      #randomize the key
      key = os.urandom(constant.KEY_BYTE)

      #reads the file as a byte 
      f = open(filepath, 'rb')
      #store the read byte into the data variable
      data = f.read()
      #always close after an open
      f.close()

      print(" > Encrypting " + filepath)
      #Run the module to get the cipher and the IV
      ct, IV = Myencrypt(data, key)

      print(" > Encryption Process Completed")
      return ct, IV, key, fExt
  else:
      print(" > Stop hallucinating, there is no " + filepath + " in this directory")

def MyRSAEncrypt(filepath, RSA_Publickey_filepath):
    C, IV, key, ext = MyfileEncrypt("./" + filepath)
        
    f=open(RSA_Publickey_filepath, 'rb')
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=b"unicorn",
        backend=default_backend()
    )
    public_key = private_key.public_key()

    #print(f.read())
 
    #encrpyt key variable ("key") using RSA publickey in OAEP padding mode
    RSACipher = public_key.encrypt(
         key,         
         asymmetric.padding.OAEP(
             mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
             algorithm=hashes.SHA256(),
             label=None
         )
    ) 

    return RSACipher, C, IV, ext
    
