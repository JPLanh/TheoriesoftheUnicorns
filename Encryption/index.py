import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

#reads the file as a byte 
f = open('traktor.jpg', 'rb')
#store the read byte into data
data = f.read()

#===================Some variables needed
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
#for the decryption part
decryptor = cipher.decryptor()
#enables our encrpytion
encryptor = cipher.encryptor()

#================== Core of it all
#This will pad the bytes and then finalize it, as in it will return the rest after the last block is done
ct = padder.update(data) + padder.finalize()
#after it has been padded, it will be encrypted.. remember since it's block it need to finish and return the rest
ct = encryptor.update(ct) + encryptor.finalize()

#Create the fake file
f = open('test.jpg', 'wb')
#write the encrypted byte into the file
f.write(ct)

#must i comment these two line? it's just the opposite
ct = decryptor.update(ct)  + decryptor.finalize()
ct = unpadder.update(ct) + unpadder.finalize()

#convert it back from a byte and make it into a image
f = open('test2.jpg', 'wb')
f.write(ct)
