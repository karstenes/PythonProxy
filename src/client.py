import ctypes
import os
import select
import socket
import ssl
import hashlib
from threading import Thread
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher import XOR
import base64

#with open('C:\\Users\\Karst\\Desktop\\privkey.txt', 'rb') as f:
    #privKey = RSA.importKey(f.read())
#with open('C:\\users\\karst\\Desktop\\pubkey2.txt', 'rb') as f:
    #pubKey = RSA.importKey(f.read())
ctypes.windll.kernel32.SetConsoleTitleA(b"Python Proxy Client")
title = lambda x: ctypes.windll.kernel32.SetConsoleTitleA(
    b"Python Proxy Client; There are currently %s connections" % bytes(x.encode('ascii')))
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 1080))
s.listen(3)
clear = lambda: os.system('cls')
BLOCK_SIZE = 32
PADDING = '{'.encode('utf-8')
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
"""pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]"""
#cipher = AES.new(b'\x01Q_\xf0\xf4\xdd\xf2\xd1r\xbfSK\xd0\x03\x95E\x96p{\t\x86\xa2\x04W0\xb5m\xf3\x002\x03r')

def encrypt(key, plaintext):
  cipher = XOR.new(key)
  return base64.b64encode(cipher.encrypt(plaintext))

def decrypt(key, ciphertext):
  cipher = XOR.new(key)
  return cipher.decrypt(base64.b64decode(ciphertext))
def listener(client, address, no):
    s = socket.socket()
    sct = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ss = sct.wrap_socket(s, do_handshake_on_connect=True)
    ss.connect(('108.41.183.93', 443))
    timer = 0
    while True:
        try:
            avail = select.select([client, ss], [], [], 5)
            if avail[0]:
                if avail[0][0] == client:
                    data = client.recv(10485760)
                    #print("data from client of connection", str(no))
                    #print(data)
                    #open('C:\\Users\\Karst\\Desktop\\log.txt', 'ab').write(encrypt('password', data))
                    #open('C:\\Users\\Karst\\Desktop\\log.txt', 'a').write(data)
                    # print("Data from client of connection number", str(no + 1))
                    # print(data)
                    if data != "":
                        timer = 0
                    else:
                        data = b''
                        timer+=1
                    if timer >= 10:
                        print("Idle for 10 seconds, terminating connection no", no)
                        break
                    # add back pubKey.encrypt(bytes(data), 'x')[0]
                    ss.send(data)
                elif avail[0][0] == ss:
                    data = ss.recv(10485760) # add back privKey.decrypt()
                    #print("data from the server of connection", str(no))
                    #print(data)
                    #open('C:\\Users\\Karst\\Desktop\\log.txt', 'ab').write(data)
                    #open('C:\\Users\\Karst\\Desktop\\log.txt', 'a').write(decrypt('RCQ2wHgx6yoU58CBcS47B4vaHkO3Prvy', data))
                    if data != "":
                        timer = 0
                    else:
                        data = b''
                        timer+=1
                    if timer >= 10:
                        open('C:\\Users\\Karst\\Desktop\\log.txt', 'a').write("terminating connection no "+str(no))
                        break
                    # print("Data from server of connection number", str(no + 1))
                    # print(data)
                    client.send(data)
            checkforhangup = select.select([client], [], [], 1)
            checkforhangup = select.select([ss], [], [], 1)
        except select.error:
            break
        except socket.error:
            break
        except Exception as e:
            open('C:\\Users\\Karst\\Desktop\\errlog.txt', 'a').write("Error in thread "+str(no)+": "+str(e)+"\r\n")
    global threads
    clear()
    print(str(len(threads) - 1), 'client(s)')
    title(str(len(threads) - 1))
    ss.close()
    client.close()
    if (len(threads) - 1) < no:
        del threads[-1]
    else:
        del threads[no]
    if len(threads) == 0:
        open('log.txt', 'a').write("All clients disconnected")
    return "Exit"


threads = []
while True:
    client, address = s.accept()
    clear()
    print(str(len(threads) + 1), 'client(s)')
    title(str(len(threads) + 1))
    threads.append(Thread(target=listener, args=(client, address, len(threads))).start())
s.close()