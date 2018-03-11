from cryptography.hazmat.primitives.asymmetric import padding, OAEP, hashes

def MyRSADecrypt(RSACipher, C, IV, ext, RSA_Privatekey_filepath):
    RSAPlain = RSA_Privatekey_filepath.decrypt(
         RSACipher,
         padding.OAEP(
             mgf=padding.MGF1(algorithm=hashes.SHA256()),
             algorithm=hashes.SHA256(),
             label=None
         )
    )
    return RSAPlain, C, IV, ext