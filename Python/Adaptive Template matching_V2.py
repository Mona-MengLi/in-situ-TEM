"""
Adaptive template matching for in-situ TEM movie alignment

Basic idea:
    For in situ Movies, since the observing subject is changing, using template matching of a unchanging template is not working,
    the matchign tamplate should change with time
Updated 08/12/2020
Created on Sun Feb 16 23:48:44
‘‘‘’’’
V2: show confidence level to allow user to select if multiple most possible sites are available
V3: extend image to avoid cropping
@author: Mona
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt
import tiffile
import easygui
import tqdm
import insitu_IO as IO
import insitu_alignment as AL
from IPython import get_ipython;   
get_ipython().magic('reset -sf')
###############################################################
## 1. Inital settings 
NOF=5 #number of frame for each template

#Read Tiff stack
path =  easygui.fileopenbox("Select the tiff stack")
# imgname='Img3.tif'
# img = tiffile.imread(imgname)
stack = tiffile.imread(path)
nFrames, h,w = stack.shape

TM = np.zeros((nFrames,3))#frame, TX,TY,max_val
pathout = path[:-4]+'_TM3.csv'
pathout2 = path[:-4]+'_TM3.tif'

################################################################
#2. Open fr0 and select ROI for template matching
img = stack[0]
r = cv2.selectROI("Select ROI, press ENTER to confirm",img,fromCenter=False,showCrosshair=False)
cv2.destroyWindow("Select ROI, press ENTER to confirm")
# Crop image
template = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]#opencv coordinate: Y,x , from upper left corner of the image 
# Display cropped image
cv2.imshow("Template, press ENTER to confirm", template)
cv2.waitKey(0)
cv2.destroyWindow("Template, press ENTER to confirm")



# ################################################################
#3. Apply template to template matching
meth='cv2.TM_CCOEFF_NORMED'
method = eval(meth)
w, h = template.shape[::-1]

for i in tqdm.tqdm(range(nFrames)):
    fr=stack[i]
    # Apply template Matching
    res = cv2.matchTemplate(fr,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    
    TM[i,0]=i
    TM[i,1]=top_left[0]
    TM[i,2]=top_left[1]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(fr,top_left, bottom_right, 255, 2)
    # plt.imshow(fr,cmap = 'gray')
    # plt.title('Frame' +str(i)+'  Detected Point')
    if i%NOF==NOF-1:
        template = fr[int(top_left[1]):int(top_left[1] + h), int(top_left[0]):int(top_left[0] + w)]#opencv coordinate: Y,x , from upper left corner of the image 
    if i == 0:            
        tiffile.imsave(pathout2,fr, append=False)
    else:            
        tiffile.imsave(pathout2,fr, append=True)


TM[:,1]=TM[0,1]-TM[:,1]
TM[:,2]=TM[0,2]-TM[:,2]

# ################################################################
#4. Apply TM to movie
#Get average to minimize total movement
TM=AL.denoiseTM(TM,5)
Mx=int(np.mean(TM[:,1]))
My=int(np.mean(TM[:,2]))
TM[:,1]=TM[:,1]-Mx
TM[:,2]=TM[:,2]-My

print("------------------------------------------")
print("Saving files~")   
plt.plot(TM[:,0],TM[:,1],'b',TM[:,0],TM[:,2],'r')
  
IO.writeCSV(pathout,TM,fmt='%1.1d')
plt.show()

AL.TranslateStack(path,TM,bg=150,extend=True)

# plt.subplot(121),plt.imshow(res,cmap = 'gray')
# plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(img,cmap = 'gray')
# plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
# # plt.suptitle(method)
# # fname=imgname[:-4]+str(method)+'.png'
# # plt.savefig(fname,format='png')
#
#plt.show()
