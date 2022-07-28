#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Add timestamp and scalebar to mp4 stack, and accelerate the movie (by fps)
-Updates
     09/09/2020: Add output to Mp4 using H264 Codec via openCV

Created on Tue Jun 18 19:49:54 2019

@author: mona
"""


import tifffile
import insitu_IO as IO
import insitu_DP as DP
import tqdm
import cv2
import numpy as np
import easygui


dt = 0.2
# dt = 0.2
#Scale=34.5 #1000KX: 49.`105, 700kX: 34.5
Scale=49.5 #1000KX: 49.`105, 700kX: 34.5

path =  easygui.fileopenbox("Select the tiff file")


# #Create timestamp format
# path = 'test_DB.tif'
# pathIndex='test_DB-index.csv'

# 
video = tifffile.imread(path)
nFrames, h,w = video.shape

def ScaleIndex(Index,sf,fpsin,fpsout):
    """
%function for calculating output array 
%Input: 
%In-input vertical array;
%sf-Speed factor;
%fpsin, fpsout- fps of input and output movie
%output: Ou - output vertical array;
"""

    nIn=len(Index)
    T_In=nIn/fpsin
    T_Out=T_In/sf
    nOut=round(T_Out*fpsout)
    Out=np.zeros((nOut,1))
    fs = round(nIn/nOut)
    if fs == 1:
        Out=Index
    else:
        k=0
        for i in range(nIn):
            if np.remainder(i,fs)==0:
                Out[k]=Index[i]
                k=k+1
    return Out


def TimestampArray(index,dt=0.2):
    #Calculate time for each frame of the movie
    #returns str array of time
    # index=DP.readcsvCol(pathIndex,col_num)
    time=[]
    for i in range(len(index)):
        t=dt*index[i]
        time.append(t)
    return time

def TimestampArrayIdx(pathIndex,dt=0.2,col_num=1):
    #Calculate time for each frame of the movie
    #returns str array of time
    index=DP.readcsvCol(pathIndex,col_num)
    time=[]
    for i in index:
        t=dt*i
        time.append(t)
    return time

# #For creat timestamp from index
# pathIndex =  easygui.fileopenbox("Select the index file")
# #
# time=TimestampArrayIdx(pathIndex,dt,col_num=1)
# np.savetxt('timeIndex.csv',time,fmt='%3.1f',delimiter=",")
# #
# timeidx = DP.readcsvCol('timeIndex.csv',0)

#For creat timestamp alone
index=range(nFrames)
timeidx = TimestampArray(index,dt)

# print("---------------------------------------------")
# print('Testing positions! ')
# img = video[0]
# IO.AddScale(img,barLen=2)
# text='0.0 s'
# IO.AddText(img,text)

# print('Check preview image, press esc to continue')
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()    
#key = input('Press 1 to contine:  ')
# clip = []
fps = int(input('Input desired output fps:'))
# dur=1/fps    
pathout =path[:-4]+'_'+str(fps)+'_St.mp4'    
pathout2 =path[:-4]+'_St.tif'    

codec  = cv2.VideoWriter_fourcc(*'H264')
out = cv2.VideoWriter(pathout, codec , fps, (w,  h))
print("---------------------------------------------")
print('Adding scalebar and time to the movie')    
for i in tqdm.tqdm(range(nFrames)):        
    img=video[i]        
    # time = i * dt    
    time = timeidx[i]
    text=str('%02.1f' %time)+' s'          
    IO.AddScale(img,scale=Scale,barLen=2)        
    IO.AddText(img,text,s=0.9)   
    # cv2.imshow('frame', img)
    out.write(img)
     
    if i == 0:            
        tifffile.imwrite(pathout2,img, append=False)
    else:            
        tifffile.imwrite(pathout2,img, append=True)
#        fr = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
#        clip.append(mp.ImageClip(fr).set_duration(dur))
#
#

# Define the codec and create VideoWriter object


out.release()
cv2.destroyAllWindows()

#    print("---------------------------------------------")
#    print('Saving output mp4 file~')
#    Outvideo = mp.concatenate_videoclips(clip, method="compose",ismask=False)#ismask=True to make grayscale
#    Outvideo.write_videofile(pathout, fps=fps,codec='libx264', bitrate='16 M',preset='ultrafast') 
print("---------------------------------------------")
print('Done! Enjoy~')
