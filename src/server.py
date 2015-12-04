import select
import socket
import ctypes
import ssl
from threading import Thread

#with open('C:\\Users\\karst\\Desktop\\privkey2.txt', 'rb') as f:
    #privKey = RSA.importKey(f.read())
#with open('C:\\users\\karst\\Desktop\\pubkey.txt', 'rb') as f:
    #pubKey = RSA.importKey(f.read())
ctypes.windll.kernel32.SetConsoleTitleA(b"Python Proxy Server")
s=socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 443))
s.listen(3)

def listener(client, address, no):
    ss=socket.socket()
    ss.connect(('127.0.0.1', 1234))
    bno=0
    while True:
        try:
            avail = select.select([client, ss], [], [], 5)
            if avail[0]:
                if avail[0][0] == client:
                    data = bytearray(client.recv(10485760)) #add back privKey.decrypt()
                    #print("Data from client of connection number",str(no+1))
                    #print(data)
                    ss.send(data)
                elif avail[0][0] == ss:
                    data = bytearray(ss.recv(10485760))
                    #print("Data from server of connection number",str(no+1))
                    #print(data)
                    client.send(data) #add back bytearray(pubKey.encrypt(bytes(data), 'x')[0])
        except select.error as e:
            break
        except socket.error as e:
            break
        except Exception as e:
            print("Error:",e)
    print("Client number",no,"disconnected")
    ss.close()
    client.close()
    global threads
    if (len(threads)-1) < no:
        del threads[-1]
    else:
        del threads[no]
    if len(threads) == 0:
        print("All connections terminated")
    return "Exit"

threads=[]
while True:
    newsock, address = s.accept()
    sct = ssl.SSLContext(protocol=ssl.PROTOCOL_SSLv23)
    sct.load_cert_chain("server.crt", keyfile="server.key", password="spr1te")
    client = sct.wrap_socket(newsock, server_side=True,do_handshake_on_connect=True)
    print("New Client Connection, number",str(len(threads)+1))
    threads.append(Thread(target=listener,args=(client, address, len(threads))).start())