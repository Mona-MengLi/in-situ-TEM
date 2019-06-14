# -*- coding: utf-8 -*-
"""
in-situ TEM Toolbox - Input Output

Assembles of functions related to movie input output

Example:
    
    import insitu_IO as IO
    IO.f2tif(path,1)

Created on Tue Jun 11 10:25:25 2019
@author: Mona
"""

import moviepy.editor as mp
#from moviepy.editor import concatenate_videoclips,ImageClip,VideoFileClip,vfx
import cv2
import tiffile
import tqdm #not necessary just provides a progress bar and timer


def f2mp4(path,fps):
    """
    function to convert any input file to H264 High quality mp4
    Inputs: filepath, output fps,is_gray: 1 for grayscale, 0 for rgb
    Output: file in the same folder named '..._cv.mp4'
    """

    print("==============================================")
    print("Convert file to MP4!")
    pathout = path[:-4]+'_'+str(fps)+'.mp4'
    if path.endswith('.tif'):            
#        import tiffile
        im = tiffile.imread(path)
        nFrames, h,w = im.shape
        fps=int(input("Enter desired fps: "))
        dur=1/fps
        clip = []
        print("---------------------")
        print("Read TIF file!")
        for i in tqdm.tqdm(range(nFrames)):
            fr = cv2.cvtColor(im[i],cv2.COLOR_GRAY2RGB)
            clip.append(mp.ImageClip(fr).set_duration(dur))
        video = mp.concatenate_videoclips(clip, method="compose",ismask=False)#ismask=True to make grayscale

    else:
        video = mp.VideoFileClip(path)
        fpsIn = int(video.fps)
        if fps != fpsIn:
            print("Conflict in fps! \n",              "[0] Use fps of input file;\n",              "[1] Use desired fps w/o speedup;\n",
              "[2] Use desired fps w/ speedup:")
            k = input('Input your selection: ')
            if k == 2:
                sf = fps/fpsIn
                video =video.fx(mp.vfx.speedx, sf)
            elif k == 0:
                fps = fpsIn
        video.reader.close()# To fix handel error problem
    print("---------------------")

    print("Save to mp4!")
    video.write_videofile(pathout, fps=fps,codec='libx264', bitrate='32 M',preset='ultrafast') 
   
    print("==============================================")
    print("MP4 convertion Done!")
    

def f2tif(path,is_gray=1):
    """
    function to convert any input file to tif stack
    Inputs: filepath, is_gray: 1 for grayscale, 0 for rgb
    
    Output: file in the same folder named '..._cv.tif'
    """   
#    import tiffile
    import tqdm
    print("==============================================")
    print("Convert file to tif stack!")
    pathout = path[:-4]+'_'+str(is_gray)+'.tif'    
    video = mp.VideoFileClip(path)
    i=0
    for fr in tqdm.tqdm(video.iter_frames()):
        if is_gray == 1:
            fr= cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY) 
        if i == 0:
            tiffile.imsave(pathout,fr, append=False)
        else:
            tiffile.imsave(pathout,fr, append=True)
        i += 1
    print("==============================================")
    print("TIF convertion Done!")
    print("nFrames="+str(i))
    video.reader.close()# To fix handel error problem


def f2gif(path,fps):
    """
    function to convert any input file to gif animation
    Inputs: filepath, output fps, is_gray: 1 for grayscale, 0 for rgb
    
    Output: file in the same folder named '..._cv.mp4'
    """
    print("==============================================")
    print("Convert file to GIF!")
    pathout = path[:-4]+'_'+str(fps)+'.gif'
    if path.endswith('.tif'):            
#        import tiffile
        im = tiffile.imread(path)
        nFrames, h,w = im.shape
        dur=1/fps
        clip = []
        for i in range(nFrames):
            fr = cv2.cvtColor(im[i],cv2.COLOR_GRAY2RGB)
            clip.append(mp.ImageClip(fr).set_duration(dur))
        video = mp.concatenate_videoclips(clip, method="compose",ismask=False)#ismask=True to make grayscale

    else:
        video = mp.VideoFileClip(path)
        fpsIn = int(video.fps)
        if fps != fpsIn:
            print("Conflict in fps! \n",              "[0] Use fps of input file;\n",              "[1] Use desired fps w/o speedup;\n",
              "[2] Use desired fps w/ speedup:")
            k = input('Input your selection: ')
            if k == 2:
                sf = fps/fpsIn
                video =video.fx(mp.vfx.speedx, sf)# Not working when sf<1
            elif k == 0:
                fps = fpsIn

    video.write_gif(pathout,fps=fps)
    video.reader.close()# To fix handel error problem
#    if path.endswith('.gif'):
#        clip.write_videofile(pathout,fps=fps,codec='libx264', bitrate='32 M',preset='ultrafast')
    print("==============================================")
    print("MP4 convertion Done!")

def gifmp4converter(path,fpsOut):
    """
    Function to convert between mp4 and gif files
    Inputs: file path; Output fps
    Output: mp4/gif file in the same folder named '..._cv.mp4/gif'
        
    Example: 
        gifmp4converter(path,25)
    """
#    import moviepy.editor as mp
    
    print("=========================================")
    print("GIF-MP4 Converter Started!")

    clip = mp.VideoFileClip(path)
    #Get output fps
    fpsIn = int(clip.fps)
    if fpsOut != fpsIn:
        print("Conflict in fps! \n",
              "[0] Use fps of input file;\n",
              "[1] Use desired fps w/o speedup;\n",
              "[2] Use desired fps w/ speedup:")
        k = input('Input your selection: ')
        if k == 2:
            sf = fpsOut/fpsIn
            fps = fpsOut                
            clip =clip.fx(mp.vfx.speedx, sf)
        elif k == 0:
            fps = fpsIn
        else:
            fps = fpsOut           
# Converting formats
    if path.endswith('.gif'):
        pathout = path[:-4]+'_cv'+'.mp4'
        clip.write_videofile(pathout,fps=fps,codec='libx264', bitrate='32 M',preset='ultrafast')
    elif path.endswith('.mp4'):
        pathout = path[:-4]+'_cv'+'.gif'
        clip.write_gif(pathout,fps=fps)
    clip.reader.close()# To fix handel error problem
    print("=========================================")
    print("GIF-MP4 Converter Done!")
    
def GetInfo(path):
    """
    function to get movie info  from any file form: mp4 , tif, gif
    Inputs: filepath
    Output: nFrames, w, h, fps
    Example: w,h,nFrames,fps = GetInfo(path)

    """   
#    import tiffile
##    import tqdm
#    import moviepy.editor as mp
#    import cv2
    if path.endswith('.tif'):
        video = tiffile.imread(path) 
        nFrames, h,w = video.shape
        fps=int(input("Enter desired fps: "))
    else:
        video = mp.VideoFileClip(path)
        fps= int(video.fps)
        nFrames = int(fps*video.duration)
        w = int(video.w)
        h = int(video.h)
        video.reader.close()# To fix handel error problem
    return w,h,nFrames,fps

def RdFr(path,i,is_gray=1):
    """
    function to read frame from any file form: mp4 , tif, gif
    Inputs: filepath, is_gray: 1 for grayscale, 0 for rgb
    
    Output: frame image fr
    Example: 
IO.fr= RdFr(path,i)
cv2.imshow('Frame'+str(i),fr)
cv2.waitKey(0)
cv2.destroyAllWindows()
    """   
#    import tiffile
##    import tqdm
#    import moviepy.editor as mp
#    import cv2
    if path.endswith('.tif'):
        video = tiffile.imread(path)
        fr = video[i]                    
    else:
        video = mp.VideoFileClip(path)
        fps= int(video.fps)
        fr = video.get_frame(mp.cvsecs(i/fps))
        if is_gray == 1:
            fr= cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        video.reader.close()# To fix handel error problem
    return fr

def ExtractFrame(path,framelist,is_gray=1):
    """
    function to Extract frame from any file format: mp4 , tif, gif
    Inputs: filepath, list of frames to be extracted
    Output: frame images saved in original folder
    Example: 
        import insitu_IO as IO
        IO.ExtractFrame(path,[0,1,10,11],0)

    """ 
    if path.endswith('.tif'):
        video = tiffile.imread(path)
    else:
        video = mp.VideoFileClip(path)
        fps= int(video.fps)
    for i in tqdm.tqdm(framelist):
        if path.endswith('.tif'):
            fr = video[i]                  
        else:
            fr = video.get_frame(mp.cvsecs(i/fps))
            if is_gray == 1:            
                fr= cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
#        fr=RdFr(path,int(i),is_gray)          
        pathout = path[:-4]+'_F'+str(i)+'.tif'
        tiffile.imsave(pathout,fr, append=False)
    if path.endswith('.tif')==0:
        video.reader.close()


#
#def Time2List()       
    
def writeCSV(pathout,data):
#    import csv
    import numpy as np
#    (length,width)=np.shape(data)
    np.savetxt(pathout, data, fmt='%1.1d', delimiter=",")    
   