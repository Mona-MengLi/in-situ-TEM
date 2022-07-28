# -*- coding: utf-8 -*-
"""

in-situ TEM Toolbox - PreProcess
By: Meng and Michael
Assembles of functions related to movie preprocess
Example:
    
    import insitu_Preprocess as PP
    PP.blur_score(image)

Created on Tue Jun 11 10:25:25 2019


"""
import numpy as np
import cv2
from scipy import signal
from PIL import Image 

def estimate_dup(A,B,threshold=1):
    """
    Function to detect if two images are duplicated
    """
    D=np.subtract(A,B)
    score=np.mean(D)#mean works better than sum due to noises
    return bool(score<threshold)


def estimate_blank(image,threshold=50):
    """
    funciton to detect blank frames
    returns 1 if is blank
    """
    score = np.sum(image[10:15,:])
    
    return bool(score < threshold)

def blur_score(image):
    """
    funciton to get blur_score of image
    returns blur score
    """
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blur_map = cv2.Laplacian(image, cv2.CV_64F)
    score = np.var(blur_map)
    return score

def median_blur (score_list, i,thrs=150,wid=21):
    """
    funciton to detect if frame i is blur
    input: score_list: 1D array of scores; i: frame number; thrs: tolerance of blur threshold; wid： median filter width
    returns 1 if is blur
    """
    medthreshold=signal.medfilt(score_list,wid)
    #The threshold should be moved because there is no need to recreate the threshold everytime
    score = score_list[i]
    medthres = medthreshold[i]+thrs
    return medthres,bool(score>= medthres)

def tiff_crop(moviepath):
    '''  
    function to crop a tiff stack
    input: path
    output: cropped tiff stack
    '''
    from skimage import io
    from tqdm import tqdm
    import tifffile
    moviepathout = moviepath[:-4] + "_Crop.Tif"
    im = cv2.imread(moviepath)
    #only reads the first image in the Tiff stack
    # Select ROI
    r = cv2.selectROI(im, False, False)
    imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    cv2.imshow("Image", imCrop)
    #Displays the cropped image
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    #Read the Tiff file properly
    im = io.imread(moviepath)
    nframes, height, width = im.shape
    iterable = range(nframes)
    
    for num in tqdm(iterable): 
        # Crop image
        imCrop = im[num, int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
     
        # Display cropped image
        
        #save cropped image
        if num == 0:                    
            tifffile.imsave(moviepathout, imCrop, append=False)
        else:
            tifffile.imsave(moviepathout, imCrop, append=True)
            
def rotateFr(im,angle=0,expand=True,bgColor=177):
    """
    funciton to rotate frame clockwise by angle degree with filled color
    input: im-greyscale image frame
    returns rotated image
    """
#    from PIL import Image
#    angle = 73
    a=360-angle
    img = Image. fromarray(im)
    fr=img.rotate(a,expand=expand,fillcolor=bgColor)
    imgRt = np.array(fr) 
    return imgRt

def removeDP(img,position):
    #remove deadpoint in greyscale image using automated color based on surounding pixels
    #position:[x1 y1 w h]
    x1=position[0]
    y1=position[1]
    w=position[2]
    h=position[3]

    x2=x1+w
    y2=y1+h
    c1=np.mean(img[y1-1,x1:x2])
    c2=np.mean(img[y2+1,x1:x2])
#    c3=np.mean(img[x1-1,y1:y2])
#    c4=np.mean(img[x2+1,y1:y2])
#    color=int((c1+c2+c3+c4)/4)
    color = int((c1+c2)/2)
#    color = 177
    cv2.rectangle(img,(x1,y1),(x2,y2),color,-1)  