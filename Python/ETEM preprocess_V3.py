# -*- coding: utf-8 -*-
"""
Code for ETEM movie pre-process

1. Crop upper boarder
2. Delete blank  frames
3. Delete duplicate frames
4. Delete blurry frames
5. Remove deadpoint
6. Rotate
Output : 
    1. greyscale Tiff Stack of the movie 
    2. Index of remaining frame numbers  in the output movie

By Meng, Micheal
Updated Jun,18,2019
Created on Tue Jun 11 00:43:53 2019

Problem:
    1. sometimes(NOT everytime) error ：OSError: [WinError 6] The handle is invalid occurs, 
    could be solved by restarting software.
V4: 20200707
New feature: auto segment files to avoid tiff stack larger than 4G

V3: 20200303 updated
New feature: average frame to enhance SNR
    
V2: 20200217 Updated
New feature: Get blur score → Input threshold → preview → confirm → Then process the movie to minimize human intervene
@author: Mona
"""

import easygui
import insitu_IO as IO
import numpy as np
import insitu_Preprocess as PP
import cv2
import tqdm
import tiffile
import matplotlib.pyplot as plt

path =  easygui.fileopenbox("Select the mp4 file")
#path='test.mp4'
# pathout = path[:-4]+'_DB.tif'
indexout=path[:-4]+'_DB-index.csv'
DBout=path[:-4]+'_DB.csv'
DBout2=path[:-4]+'_Blur.csv'
AveN=1
#threshold=70 #Blur threshold
print("=========================================")
print("ETEM movie preprocessor start!")

import moviepy.editor as mp
import moviepy.video.fx.all as vfx

video = mp.VideoFileClip(path)
# video = video.subclip(0,154)# cut the clip between t=0 and 28 secs.
fps = int(video.fps)
w = int(video.w)
h = int(video.h)
nFrames = int(fps*video.duration)
video =  (video.fx(vfx.crop, x1=0, y1=28, x2=w-3, y2=h-4))#crop movie old
# video =  (video.fx(vfx.crop, x1=0, y1=45, x2=w-3, y2=h-4))#crop movie old

# video =  (video.fx(vfx.crop, x1=0, y1=25, x2=w-3, y2=h-4))#crop movie new
# DP=[367, 441, 4, 4]#Cu0Ni
DP= [364, 438, 4, 4] #old Cu
# DP= [358, 432, 4, 4] #old Cu

#angle = int(input('input rotate angle:(clockwise)  '))

#Preview first frame
print("------------------------------------------")
print("Preview the processed frame: close window to continue")
fr = video.get_frame(mp.cvsecs(0/fps))
fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
#PP.remove4) #Cu
PP.removeDP(fr,DP)#CuNi
#PP.removeDP(fr,394, 474, 398, 478)#Cu
# PP.removeDP(fr,366, 440, 370, 480)

#fr=PP.rotateFr(fr,angle)
#fr.show()
IO.showFr(fr)
#cv2.imshow('Check croped Frame0',fr)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
print("------------------------------------------")
print("Detecting blank and duplicate frames, calculating blur scores~")
DB=np.zeros((nFrames,4)) #[i,is_blank,is_dup,score]
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
        is_dup = PP.estimate_dup(fr,nxfr,2)
        DB[i,2]=is_dup
        if is_dup ==0:
            s = PP.blur_score(fr)
            score.append(s)
            index.append(i)

            DB[i,3] = s
            
length = len(score)
Blur=np.zeros((length,3))#[i,blur_score,blur_th]
Blur[:,0]=index
Blur[:,1]=score            
IO.writeCSV(DBout2,Blur)     


plt.plot(score,'gray')
plt.show()     

#threshold=int(input("input threshold for blur detection: (default=70)"))
  

#print("------------------------------------------")200
#print("Detecting blurry frames~")   
#for i in tqdm.tqdm(range(len(score))):
#    medthres,is_blur=PP.median_blur (score, i,threshold,wid=20)
#    DB[index[i],3]=is_blur
#    Blur[i,2]=medthres
#    if is_blur == 0:
#        index2.append(index[i])
#        
##        
##IO.writeCSV(DBout2,Blur)     
##   
#plt.plot(Blur[:,0],Blur[:,1],'gray',Blur[:,0],Blur[:,2],'r')
#plt.show()

print("------------------------------------------")
print("Check blur detection!")  
#thrs = 70;
thrs=int(input( 'Input blur threshold(default: 70): ')) 
while thrs!=0:
    index2=[]

    for i in tqdm.tqdm(range(len(score))):
        medthres,is_blur=PP.median_blur (score, i,thrs,wid=21)#wid must be odd
#        DB[index[i],3]=is_blur
        Blur[i,2]=medthres
        if is_blur == 0:
            index2.append(index[i])
            
    plt.plot(Blur[:,0],Blur[:,1],'gray',Blur[:,0],Blur[:,2],'r')
    plt.show()
    thrs=int(input( 'press 0 if you are satisfied, press corrected threshold if you want to change:  ')) 
   
IO.writeCSV(DBout2,Blur)  
    
result= np.zeros((len(index2),3)) 
for i in range(len(index2)):
    result[i,0]=i
    result[i,1]=index2[i]
#    result[i,2]=score[index2[i]]
    
IO.writeCSV(indexout,result)

import math

nFramesOut=math.floor(len(index2)/AveN)

print("------------------------------------------")
print("Saving files~")   
# for i in tqdm.tqdm(range(nFramesOUt)):
pathout=path[:-4]+'_DB2.tif'
for i in tqdm.tqdm(range(0,len(index2),AveN )):
    fr = video.get_frame(mp.cvsecs(index2[i*AveN]/fps))
    fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)  
    # PP.removeDP(fr,364, 438, 368, 442)
    PP.removeDP(fr,DP)#CuNi

    # nxfr = video.get_frame(mp.cvsecs(index2[i*AveN+1]/fps))
    # nxfr = cv2.cvtColor(nxfr, cv2.COLOR_BGR2GRAY)
    # PP.removeDP(nxfr,364, 438, 368, 442)\
    # PP.removeDP(fr,DP)#CuNi
    # AveFr=fr/2+nxfr/2
    # fr = AveFr.astype(np.uint8)
    if i>4000:
        
        j= i-4001
    else:
        j=i
     
    if i == 0 or j==0:
        tiffile.imsave(pathout,fr, append=False)
    else:
        tiffile.imsave(pathout,fr, append=True)
 

    

#IO.writeCSV(DBout,Blur)
    

print("=========================================")
print("All done! Enjoy~")
video.reader.close()
