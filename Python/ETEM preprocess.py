# -*- coding: utf-8 -*-
"""
Code for ETEM movie pre-process

1. Crop upper boarder
2. Delete blank  frames
3. Delete duplicate frames
4. Delete blurry frames

Output : 
    1. greyscale Tiff Stack of the movie 
    2. Index of remaining frame numbers  in the output movie

By Meng, Micheal
Created on Tue Jun 11 00:43:53 2019

Problem:
    1. sometimes(NOT everytime) error ：OSError: [WinError 6] The handle is invalid occurs, 
    could be solved by restarting software.
@author: Mona
"""

import easygui
import insitu_IO as IO
import insitu_DP as DP
import numpy as np
import insitu_Preprocess as PP
import cv2
import tqdm
import tiffile

path =  easygui.fileopenbox("Select the mp4 file")
pathout = path[:-4]+'_DB.tif'
indexout=path[:-4]+'_DB-index.csv'
DBout=path[:-4]+'_DB.csv'

print("=========================================")
print("ETEM movie preprocessor start!")

import moviepy.editor as mp
import moviepy.video.fx.all as vfx

video = mp.VideoFileClip(path)
fps = int(video.fps)
w = int(video.w)
h = int(video.h)
nFrames = int(fps*video.duration)
video =  (video.fx(vfx.crop, x1=0, y1=28, x2=w-2, y2=h-4))#crop movie

##Preview first frame
#fr = video.get_frame(mp.cvsecs(0/fps))
#fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
#cv2.imshow('Check croped Frame0',fr)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
print("------------------------------------------")
print("Detecting blank and duplicate frames~")
DB=np.zeros((nFrames,4)) #[i,is_blank,is_dup,is_blur]
index = []#index of remaining frames
score = []
#Remove blank and dup frames
for i in tqdm.tqdm(range(nFrames-1)):
    fr = video.get_frame(mp.cvsecs(i/fps))   
    fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    nxfr = video.get_frame(mp.cvsecs((i+1)/fps))   
    nxfr = cv2.cvtColor(nxfr, cv2.COLOR_BGR2GRAY)
    is_blank = PP.estimate_blank(fr)
    DB[i,0]=i
    DB[i,1]=is_blank
    if is_blank == 0:
        is_dup = PP.estimate_dup(fr,nxfr,1)
        DB[i,2]=is_dup
        if is_dup ==0:
            s = PP.blur_score(fr)
            score.append(s)
            index.append(i)
        else:
            DB[i,3] = 1
    else:
        DB[i,2]=1
        DB[i,3] = 1
        

  

print("------------------------------------------")
print("Detecting blurry frames~")   
length = len(score)
index2=[]
for i in tqdm.tqdm(range(len(score))):
    is_blur=PP.median_blur (score, i,200)
    DB[index[i],3]=is_blur
    if is_blur == 0:
        index2.append(index[i])
        

print("------------------------------------------")
print("Saving files~")   
for i in tqdm.tqdm(range(len(index2))):
    fr = video.get_frame(mp.cvsecs(index2[i]/fps))   
    fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    if i == 0:
        tiffile.imsave(pathout,fr, append=False)
    else:
        tiffile.imsave(pathout,fr, append=True)

    
result= np.zeros((len(index2),2)) 
for i in range(len(index2)):
    result[i,0]=i
    result[i,1]=index2[i]
    
IO.writeCSV(indexout,result)
IO.writeCSV(DBout,DB)
    

print("=========================================")
print("All done! Enjoy~")
video.reader.close()
