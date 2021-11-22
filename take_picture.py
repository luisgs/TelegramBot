# import libraries
import time
import os

download_dir = "/home/osmc/Pictures/webcam/"

def take_1_pic():
    path_to_pic = download_dir +'%d%m%y_%H%M%S.jpg'
    os.system('fswebcam -S 100 --save ' + path_to_pic)
    return path_to_pic


def path_to_pic():
    return take_1_pic


take_1_pic()
