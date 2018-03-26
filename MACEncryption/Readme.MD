# Encrpytor / Decryptor (now with MAC WOW!)

## Synopsis
Using only hazmat we are to implement a ransomware that encrypts a chosen file with CBC (AES_MODE), and then at a later time decrypt the same file back to it's original file, all using HMAC 

## Instructions
Place all file in a desired directory to encrypt/decrypt. Then execute Main.py and simply type the command upon prompted.
### encrypt (filename) + .(ext)
    ex. encrypt traktor.jpg
### decrypt (filename)
    ex. decrypt traktor
Note: decrypt command does not need the extension, it only requires the filename as it will help the program to determine if we encrypted it.
### create unicorn
    ex. create unicorn
Note: This is only to generate a new public and private key and create their respective .pem files
Note II: If a private.PEM exist, it will create a public.PEM from it so that way you can encrypt files with the same key leaving less trace (although this might be considered recyling)

## Authors
### Jimmy Lanh
### Kelly Hall
