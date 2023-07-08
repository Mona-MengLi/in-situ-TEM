# -*- coding: utf-8 -*-
"""
Detect blur frames using FFT

Created on Mon Apr 19 16:06:06 2021

@author: Mona
"""
import easygui
import insitu_IO as IO
import numpy as np
import insitu_Preprocess as PP
import insitu_DP as DP
import cv2
import tqdm
import tifffile
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
import matplotlib.pyplot as plt

path =  easygui.fileopenbox("Select the tiff stack")
im = tifffile.imread(path)
# im = tiffile.imread(path)
nFrames, h,w = im.shape
pathout = path[:-4]+'_DP.tif'
#path='test.mp4'
# pathout = path[:-4]+'_DB.tif'
indexout=path[:-4]+'_DB-index.csv'
DBout=path[:-4]+'_DB.csv'
DBout2=path[:-4]+'_Blur.csv'
AveN=1

print("------------------------------------------")
print("Calculating blur scores~")
DB=np.zeros((nFrames,4)) #[i,is_blank,is_dup,score]
index = []#index of remaining frames
score = []

#Remove blank and dup frames
for i in tqdm.tqdm(range(nFrames-1)):
    fr=im[i]
    s=PP.blur_score(fr)
    score.append(s)
    index.append(i)


Blur=np.zeros((nFrames,3))#[i,blur_score,blur_th]
Blur[:,0]=index
Blur[:,1]=score            
# IO.writeCSV(DBout2,Blur)     
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
    

plt.plot(score,'gray')
plt.show()     
