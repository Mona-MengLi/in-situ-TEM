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

def median_blur (score_list, i,tor=20):
    """
    funciton to detect if frame i is blur
    input: score_list: 1D array of scores; i: frame number; tor: tolerance of blur threshold
    returns 1 if is blur
    """
    medthreshold=signal.medfilt(score_list,15)
    #The threshold should be moved because there is no need to recreate the threshold everytime
    score = score_list[i]
    medthres = medthreshold[i]+tor
    return bool(score >= medthres)

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