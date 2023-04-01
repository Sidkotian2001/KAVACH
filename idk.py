# import sys

# data=[]
# for line in sys.stdin:
#     l = line
#     data.append(l)
#     print("----->",l)

# print(data)
# from ultralytics import YOLO
# import supervision as sv
# import os
# path = os.path.dirname(ultralytics.__file__)


import subprocess
import tempfile

with tempfile.TemporaryFile() as tempf:
    proc = subprocess.Popen(['echo', 'a', 'b'], stdout=tempf)
    proc.wait()
    tempf.seek(0)
    print (tempf.read())
