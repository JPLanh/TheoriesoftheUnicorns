import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

#not sure about this part
backend = default_backend()
#randomize the key, but not sure if it is suppose to be this way because we will need to reuse it for later
key = os.urandom(32)
#randomize the iv, but not sure if it suppose to be this way because we will need to reuse it for later
iv = os.urandom(16)
#initalize the padder because CBC needs a padder
padder = padding.PKCS7(128).padder()
#as we pad thing we have to unpad them
unpadder = padding.PKCS7(128).unpadder()

#it's a method to use all the keys to cipher them the first two parameter uses the libraries to implement AES and CBC using our key and IV
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
#enables our encrpytion
encryptor = cipher.encryptor()
#the b just make it a byte, but this will pad out the message and finalize it just to finish the operation to return the rest of the block
ct = padder.update(b"hi a Simple message, and my name is jimmy") + padder.finalize()
#after it has been padded, it will be encrypted.. remember since it's block it need to finish and return the rest
ct = encryptor.update(ct) + encryptor.finalize()
print(ct)
#for the decryption part
decryptor = cipher.decryptor()
#must i really comment the rest? it's in reverse..
ct = decryptor.update(ct)  + decryptor.finalize()
ct = unpadder.update(ct) + unpadder.finalize()
#convert it back from a byte to string
print(str(ct, 'utf-8'))
