import os
from glob import glob
import encrypt
import decrypt

flag = True;

while(flag):
  
  print("Options:")
  print("encrypt [filename]")
  print("decrypt (filename)")
  print("quit")
  getInput = input("Command: ")

  if len(getInput.split(" ")) == 2:
    cmd,file = getInput.split(" ")
    if cmd == "encrypt":
      encrypt.MyfileEncrypt("./" + file)
    elif cmd == "decrypt":
      decrypt.MyfileDecrypt("./" + file)      
  elif (len(getInput.split(" ")) == 1):
     if getInput == "quit":
       flag = False;
       print("Good bye")
  else:
    print("Invalid command")