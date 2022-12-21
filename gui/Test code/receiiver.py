from __future__ import division
import cv2
import numpy as np
import socket
import struct
from iris_local_kivy import iris_voice

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
    print('Enter dump buffer')
    # dump_buffer(s)
    print('Exit dump buffer')
    iris_obj = iris_voice()
    i = 0
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        # if struct.unpack('B', seg[0:1])[0] > 1:
        #     dat += seg[1:]
        # else:
        dat += seg[1:]
        img = cv2.imdecode(np.frombuffer(dat, dtype=np.uint8), 1)
        number_of_eyes_captured = 0
        if i == 300:
            number_of_eyes_captured += 1
            i = 0
        new_frame = iris_obj.capture(img, number_of_eyes_captured)
        cv2.imshow('frame', new_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        dat = b''
        i += 1
    # cap.release()
    cv2.destroyAllWindows()
    s.close()

if __name__ == '__main__':
    main()
