# Python package for in-situ TEM movie process


Install the insitu toolbox via pipinstall insituTEM

Download and run Name.py / ipynb  as the specific code for the purpose specified in the name and first few lines of the code

A typical workflow is: 
1. ETEM preprocess : this code converts the movie into Tiff stack, detects and deletes blurry frames and keep track of the indexes of each remaining frame.
2. Adaptive template matching: This code performs adaptive template matching to get atomically aligned frames
3. Other processing steps such as segmentation/ quantification.. 
4. AddScaleTime: Output the processed movie into .mp4 file and tiff stack with scale bars and timestamp

--------------------------------------
Prerequsted packages:  (could by installed using 'pip install XXX')
1. moviepy
2. tifffile
3. easygui
4. cv2 
5. tqdm
6. numpy


