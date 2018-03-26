import os
import glob
import json
import constant
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import asymmetric, hmac, serialization, padding, hashes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.exceptions import InvalidSignature

def MydecryptMAC(cipherText, iv, EncKey, HMACKey, tag):
    newTag = hmac.HMAC(HMACKey, hashes.SHA256(), backend=default_backend())
    newTag.update(cipherText)
    try:
        #We can test the varification by changing the tag to some other type of byte,
        #i.e. b"hi"
        newTag.verify(tag)
        #method to use all the keys to cipher them, the first to parameters uses the hazmat's libraries 
        #to implement AES and CBC using our key and IV
        cipher = Cipher(algorithms.AES(EncKey), modes.CBC(iv), backend=default_backend())
        
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
    except InvalidSignature:
        return None
  
def MyfileDecryptMAC(filepath):
  print(" > Locating magical unicorns")
  #break the file name to two parts, the name and extension

  #check if file exists
  #if yes, read the file, load the JSon content and close the file
  if os.path.isfile(filepath):
    print(" > magical unicorn found")

    jread = open(filepath)
    fName, fExt = os.path.splitext(os.path.basename(filepath))

    
    #separate JSon data into their respective variables
    jsonStuff = json.load(jread)
    jread.close()
    data = b64decode(jsonStuff["cipher"])
    RSACipher = b64decode(jsonStuff["key"])
    IV = b64decode(jsonStuff["iv"])
    tag = b64decode(jsonStuff["tag"])
    ext = jsonStuff["ext"]

    RSA_Privatekey_filepath=os.getcwd() + "/" + constant.PRIVATE_PEM

    #Decrypt the RSACipher
    pt, ext = MyRSADecryptMAC(RSACipher, data, IV, tag, ext, RSA_Privatekey_filepath)

    if pt == None:
        print(" > OMG someone hacked the unicorn")
    else:        
        print(" > Managing all files")
        
        #convert it back from a byte and make it into a image
        f = open(fName + ext, 'wb')
        f.write(pt)
        f.close()
        os.remove(filepath)
        
        #announce completion of encryption and return pt and variable associated with 'ext'
        print(" > Encryption process complete")
  
  #else if file does not exist
  else:
    print("File does not exist, or it wasn't our fault that this file was corrupted because we did not touch it")


def MyRSADecryptMAC(RSACipher, C, IV, tag, ext, RSA_Privatekey_filepath):

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

    #because we concatoned the two key during out RSAEncryption phase, we had to split
    #it up so we can get both the key and the HMACKey
    keySet = key.split("unicorn".encode())
    EncKey = keySet[0]
    HMACKey = keySet[1]

    
    #call Mydecrypt using C, key, and IV to finally receive the original file again
    #announce decryptionn
    print(" > Decrypting filepath")
    pt = MydecryptMAC(C, IV, EncKey, HMACKey, tag)

    if pt == None:
        return None, None
    else:
        return pt, ext
