from cryptography.hazmat.primitives.asymmetric import padding, OAEP, hashes


def MyRSAEncrypt(key, C, IV, ext, RSA_Publickey_filepath):
    RSACipher = RSA_Publickey_filepath.encrypt(
         key,
         padding.OAEP(
             mgf=padding.MGF1(algorithm=hashes.SHA256()),
             algorithm=hashes.SHA256(),
             label=None
         )
    )

    return RSACipher, C, IV, ext