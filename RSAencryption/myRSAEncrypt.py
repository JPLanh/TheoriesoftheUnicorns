from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

class MyRSAEncrypt():
	RSA_Publickey_filepath = None

	RSA_Privatekey_filepath = rsa.genearte_private_key(
					public_exponent =65537
					key_size=2048
					backend=default_backend()
				) 

	def encrypt():
		return 0

	def decrypt():
		return 0	


	#first call MyfileEncrypt(filepath) which will return (C, IV, key, ext)
	#C, IV, key, ext = MyfileEncrypt(filepath)

	#init RSA public key encryption object
	#load pem publickey from the RSA_publickey_filepath
	#encrpyt key variable ("key") using RSA publickey in OAEP padding mode
	#result will be RSACipher
	#return (RSACipher, C, IV, ext)
	
	#do inverse:
	#MyRSADecrypt(RSACipher, C, IV, ext, RSA_Privatekey_filepath)
	#which does exactly the inverse of the above 
	#generate the decrypted file using your previous decryption methods
