import os
import time
from cv2 import cv2
import socket
import base64

aux = 0
texto = ''
diretorio = './Imagens'
HOST = '192.168.1.102'
PORT = 65000
texto = ''
str1 = ''
data = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

for f in os.listdir(diretorio):#Lista todos os arquivos do diretório
    os.remove(os.path.join(diretorio,f))#remove todas as imagens do diretório

camera = cv2.VideoCapture("http://192.168.1.100:8080/video")

while (True):
    _, img = camera.read()
    ini = time.time()
    #cv2.imshow('Camera', img)
    src = './Imagens/'+texto+'.png'
    texto = str(aux) #transforma o numero em string
    cv2.imwrite(src, img)
    imgUMat = cv2.imread(src)
    resized = cv2.resize(imgUMat, (32, 32), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(src, gray)
    with open(src, "rb") as imageFile:
        str1 = base64.b64encode(imageFile.read())
    print(len(str1))
    s.sendall(str1)
    #time.sleep(2)
    if aux == 20:
        for f in os.listdir(diretorio):#Lista todos os arquivos do diretório
            os.remove(os.path.join(diretorio,f))
        aux = 0
    aux = aux + 1
        
    

#cv2.destroyAllWindows()
camera.release()