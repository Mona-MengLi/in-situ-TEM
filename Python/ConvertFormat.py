# -*- coding: utf-8 -*-
"""
Example code to convert format of movie/tif/gif  using insitu_IO
Created on Tue Jun 11 00:43:53 2019

@author: Mona
"""

import easygui
import insitu_IO as IO



path = easygui.fileopenbox("Select the GIF/mp4 file") #for UI file selection

## Uncomment below to use each function

##Example to extract selected frames from movie
#framelist=[2,11,110]
#IO.ExtractFrame(path,framelist,is_gray=0)

## Example to convert movie to tiff stack 
#IO.f2tif(path,1) #1- greyscale, 0- rgb color

## Example to convert tiff/ gif to mp4
#IO.f2mp4(path,fps)

## Example to convert tiff/ mp4 to gif 
#IO.f2gif(path,fps)

