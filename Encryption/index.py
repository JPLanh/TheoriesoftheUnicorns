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
#the b just make it a byte, but this will pad an encrypt it all at once
ct = encryptor.update(padder.update(b"hi a Simple message, and my name is jimmy")) + encryptor.finalize() + padder.finalize()
print(ct)
#for the decryption part
decryptor = cipher.decryptor()
#take our encrypted message and decrypt it... unpad it and finalize it
ct = decryptor.update(unpadder.update(ct)) + decryptor.finalize() + unpadder.finalize()
print(ct)
