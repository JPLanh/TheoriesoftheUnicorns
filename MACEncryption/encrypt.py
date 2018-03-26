import os
from base64 import b64decode
import constant
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives import serialization, hashes, hmac, asymmetric, padding

def MyencryptMAC(message, EncKey, HMACKey):
    if (len(EncKey) == constant.KEY_BYTE_REQUIREMENT):
        if (len(HMACKey) == constant.KEY_BYTE_REQUIREMENT):
          backend = default_backend()
          #Randomize the IV with the specified IV_BYTE
          IV = os.urandom(constant.IV_BYTE)
      
          #method to use all the keys to cipher them, the first two parameter uses the hazmat's libraries to implement AES and CBC using our key and IV
          C = Cipher(algorithms.AES(EncKey), modes.CBC(IV), backend=backend)
            
          #initalize the padder because CBC needs a padder
          padder = padding.PKCS7(constant.PADDING_BLOCK_SIZE).padder()

          #enables our encrpytion
          encryptor = C.encryptor()

          #================== Core of it all
          #This will pad the bytes and then finalize it, as in it will return the rest after the last block is done
          ct = padder.update(message) + padder.finalize()
          #after it has been padded, it will be encrypted.. remember since it's block it need to finish and return the rest
          ct = encryptor.update(ct) + encryptor.finalize()

          #HMAC portion
          tag = hmac.HMAC(HMACKey, hashes.SHA256(), backend=default_backend())
          tag.update(ct)
          tag = tag.finalize()

          print(" > Encryption complete")
          return ct, IV, tag
        else:
          raise ValueError('There is a hacker on the loose trying to steal teh code')            
    else:
      #Intentional mispell for the fun
      raise ValueError('There is a hacker on the loose trying to steal teh code')

def MyfileEncryptMAC(filepath):

  print(" > Opening " + filepath)
  try:
      os.path.isfile(filepath)
      #break the file name to two parts, the name and extension
      fName, fExt = os.path.splitext(os.path.basename(filepath))
      #randomize the key
      EncKey = os.urandom(constant.KEY_BYTE)
      HMACKey = os.urandom(constant.KEY_BYTE)
      
      #reads the file as a byte 
      f = open(filepath, 'rb')
      #store the read byte into the data variable
      data = f.read()
      #always close after an open
      f.close()

      print(" > Encrypting " + filepath)
      #Run the module to get the cipher and the IV
      ct, IV, tag = MyencryptMAC(data, EncKey, HMACKey)
    
      print(" > Encryption Process Completed")
      return ct, IV, tag, EncKey, HMACKey, fExt
    
  except FileNotFoundError:
      print(" > Stop hallucinating, there is no " + filepath + " in this directory")    
      return None, None, None, None, None, None
    
def MyRSAEncryptMAC(filepath, RSA_Publickey_filepath):
    #call MyfileEncrypt to get varables, C, IV, Key, ext
    #and encrypt file as per method
    C, IV, tag, EncKey, HMACKey, ext = MyfileEncryptMAC("./" + filepath)
    if C != None:
        f=open(RSA_Publickey_filepath, 'rb')
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
     
        #encrpyt key variable ("key") using RSA publickey in OAEP padding mode
        RSACipher = public_key.encrypt(
             EncKey+"unicorn".encode()+HMACKey,         
             asymmetric.padding.OAEP(
                 mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
                 algorithm=hashes.SHA256(),
                 label=None
             )
        ) 

        return RSACipher, C, IV, tag, ext
