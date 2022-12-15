import cv2
import math
import struct
import socket
'''
Object to break down image frame segment
if the size of image exceed maximum datagram size 
'''
MAX_DGRAM = 2**16
MAX_IMAGE_DGRAM = MAX_DGRAM - 64 # minus 64 bytes in case UDP frame overflown
class FrameSegment(object):
  
  
  def __init__(self, sock, port, addr='192.168.237.170'):
    self.s = sock
    self.port = port
    self.addr = addr
  def udp_frame(self, img):
    ''' 
    Compress image and Break down
    into data segments 
    '''
    compress_img = cv2.imencode('.jpg', img)[1]
    dat = compress_img.tobytes()
    size = len(dat)
    num_of_segments = math.ceil(size/(MAX_IMAGE_DGRAM))
    array_pos_start = 0
    
    while num_of_segments:
      array_pos_end = min(size, array_pos_start + MAX_IMAGE_DGRAM)
      self.s.sendto(
                   struct.pack('B', num_of_segments) +
                   dat[array_pos_start:array_pos_end], 
                   (self.addr, self.port)
                   )
      array_pos_start = array_pos_end
      num_of_segments -= 1

def main():
  ''' Top level main function '''
  # Set UDP socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  port = 12348
  fs = FrameSegment(s, port)
 
  cap = cv2.VideoCapture(0)
  while (cap.isOpened()):
    _, frame = cap.read()
    fs.udp_frame(frame)
 
  cap.release()
  cv2.destroyAllWindows()
  s.close()

if __name__ == '__main__':
  main()
