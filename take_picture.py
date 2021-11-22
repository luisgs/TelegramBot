# import libraries
from datetime import datetime
import os

download_dir = "/home/osmc/Pictures/webcam/"

def take_1_pic():
    now = datetime.now()
    path_to_pic = download_dir + now.strftime("%d%m%y_%H%M%S") + ".jpg"
    os.system('fswebcam -r 640x480 -S 100 --save ' + path_to_pic)
    return path_to_pic


def path_to_pic():
    return take_1_pic()

# testing
# take_1_pic()
