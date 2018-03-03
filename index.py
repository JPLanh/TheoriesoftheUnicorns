import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

backend = default_backend()
key = os.urandom(32)
iv = os.urandom(16)

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
encryptor = cipher.encryptor()
ct = encryptor.update(b"a Simple message") + encryptor.finalize()
print(ct)
decryptor = cipher.decryptor()
ct = decryptor.update(ct) + decryptor.finalize()
print(ct)
