from __future__ import division
import cv2
import numpy as np
import socket
import struct

MAX_DGRAM = 2**16

def dump_buffer(s):
    '''Emptying buffer frame'''
    seg, addr = s.recvfrom(MAX_DGRAM)
    print(seg[0])
    if struct.unpack('B', seg[0:1])[0] == 1:
        print('finish emptying buffer')
	
def main():
    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('192.168.237.170', 12348))
    dat = b''
<<<<<<< HEAD
    print('Enter dump buffer')
    # dump_buffer(s)
    print('Exit dump buffer')
    iris_obj = iris_voice()
    i = 0
=======
    dump_buffer(s)
>>>>>>> parent of 3c9b8d4... integrated gui with mediapipe
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        if struct.unpack('B', seg[0:1])[0] > 1:
            dat += seg[1:]
        else:
            dat += seg[1:]
            img = cv2.imdecode(np.fromstring(dat, dtype=np.uint8), 1)
            cv2.imshow('frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            dat = b''
    # cap.release()
    cv2.destroyAllWindows()
    s.close()

if __name__ == '__main__':
    main()
