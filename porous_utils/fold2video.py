
# coding: utf-8

# In[4]:

import os, glob
import numpy as np
import itertools
import shutil
import argparse

def dir_exist(dir_out):
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)

def readfiles(dir_in):
    lfolders = glob.glob(f'{dir_in}/folder*')
    lfiles = []
    
    for i in range(len(lfolders)):
        lfiles.append(glob.glob(f'{lfolders[i]}/*jpg'))
    lfiles = list(itertools.chain.from_iterable(lfiles))

    lfiles = sorted(lfiles, key=os.path.getmtime)
    return lfiles

def copyfiles(lfiles, dir_temp, fps, t):
    if len(lfiles)>t*fps:
        df = len(lfiles)//(t*fps)
    else:
        df = 1
    lfiles = np.array(lfiles)[::df]
    dir_exist(dir_temp)
    for i in range(len(lfiles)):
        shutil.copy2(lfiles[i], os.path.join(dir_temp, str(i)+'.jpg'))
        
def create_video(dir_in, dir_temp, fps):
    os.system(f'ffmpeg -r {fps} -f image2 -i {dir_temp}/%d.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p {dir_in}.avi')
    
def remove_dir_temp(dir_temp):
    shutil.rmtree(f'{dir_temp}')
    
def main(dir_in, dir_temp, fps, t):
    
    lfiles = readfiles(dir_in)
    copyfiles(lfiles, dir_temp, fps, t)
    create_video(dir_in, dir_temp, fps)
    remove_dir_temp(dir_temp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Script to generate video from images in folder given as a parameter.
        
        Example:
        folder2video plaster_2017_10_20 
        
        One can determine fps and time of video:
        folder2video plaster_2017_10_20 -fps 50 -t 20
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('dir_in', help='input directory')
    parser.add_argument('-fps', '--frames_per_second', help='frames per second', default='50')
    parser.add_argument('-t', '--time', help='time of video in seconds', default='20')
    args = parser.parse_args()
    
    dir_temp = 'video_temp'
    main(args.dir_in, dir_temp, int(args.frames_per_second), int(args.time))
    

'''
dir_in = 'plaster_2017_10_20'
dir_temp = 'video_temp'
fps = 50 # ilość klatek na sekundę
t = 20 # czas filmu 

main(dir_in, dir_temp, fps, t)
'''

