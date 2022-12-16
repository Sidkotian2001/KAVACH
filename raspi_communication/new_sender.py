import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code
cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.237.170',5002))
while True:
    ret,frame=cap.read()
    data = pickle.dumps(frame) ### new code
    if len(data) < (1<<16 - 1):
        clientsocket.sendall(struct.pack("H", len(data)) + data) ### new code
