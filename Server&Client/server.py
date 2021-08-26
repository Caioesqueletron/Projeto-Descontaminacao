import os
import socket
import base64
import time

HOST = '192.168.1.101'
PORT = 65000
texto = ''
data = ''
diretorio = './Imagens2'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print('Aguardando conexão de um cliente')
conn, ender = s.accept()
print('Conectado em', ender)
aux = 0
while True:
    data = conn.recv(50000)
    print(len(data))
    texto = str(aux)
    src = './Imagens2/' + texto + '.png'
    fh = open(src, "wb")
    fh.write(base64.b64decode(data))
    #time.sleep(2)
    fh.close()
    if aux == 50:
        for f in os.listdir(diretorio):
            os.remove(os.path.join(diretorio, f))
        aux = -1;
        break
    aux = aux + 1

conn.close()