# -*- coding: utf-8 -*-
"""
in-situ TEM Toolbox - Data process 

Assembles of functions related to movie input output

Example:
    
    import insitu_DP as DP
    IO.f2tif(path,1)

Created on Tue Jun 11 10:25:25 2019
@author: Mona
"""
import numpy as np

def readcsvCol(path,col):
    """
    Function to read csv rol into array 
    Inputs: file path; col number
    Output: 1D np array
        
    Example: 
        x = readcsvCol(path,1)
    """
    import csv
    x=[]
    with open(path,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[col]=='':
                x.append(np.nan)
            else:
                x.append(float(row[col]))
#        plt.plot(x,y) #to check if  the read  result is correct
    return x
def readcsv(path,col_list):
    """
    Function to read csv rol into array 
    Inputs: file path; col number list
    Output: 1D np array
        
    Example: 
        x = readcsv(path,[0:3])
    """
#    w= len(col_list)
    x=readcsvCol(path,col_list[0])
#    l = len(x)
    D=np.zeros((len(x),len(col_list)))
    i=0
    for col in col_list:
        
        x=readcsvCol(path,col)
        D[:,i]=x
        i=i+1
#        D = [D, x]
    return D

    
def writeCSV(pathout,data):
#    import csv
    import numpy as np
#    (length,width)=np.shape(data)
#    np.savetxt(pathout, data, fmt='%1.4d', delimiter=",") 
    np.savetxt(pathout, data, fmt='%.4f', delimiter=",")   
    
def plot2ani(x,y,outpath,label,w=800,h=600,fps=10,dpi=72,tl_size=20,c='r'):
    """
    Function to make plot into animation 
    Inputs: 
        data: x y; 
        Movie setting: size: w,h ;
                       fps; savepath
                       label: ['xlabel','ylabel'] str array
                       tl_size: title font size
                       c: color of the plot line
                       dpi: dpi for screen : 72 for 4k screen, 96 for 1080p screen
    Output: mp4 movie
        
    Example: 
        plot2ani(x,y,w,h,fps,outpath,dpi,tl_size,'r')

    """
    
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    interV=1000/fps #time interval for each frame: ms
#    w_in=w/dpi
#    h_in=h/dpi
    fig, ax = plt.subplots(figsize=(w/dpi, h/dpi))#figsize unit: inch
    plt.rcParams.update({'font.size': tl_size})
    plt.xlabel(label[0])#Change xy label if needed
    plt.ylabel(label[1])
    l=plt.plot(x,y,'grey') #For inital plot
    redLine, = plt.plot(x[:0],y[:0],color=c, lw=3)
    time_text = ax.text(5,7,str(y[0])+'°',fontsize=20)
#    plt.text(5, 7, str(y[0],fontsize=20))
    def animate(i):
        redLine.set_data(x[:i], y[:i])
#        plt.text(5, 7, str(y[i])+'°',fontsize=20) # Text is overlapping with previous frames
        time_text.set_text(str(round(y[i],1))+'°') 
#        print(str(i)/len(x))
        return tuple([redLine,]) + tuple([time_text])
    
    plt.tight_layout() #To avoid boarder
    # create animation using the animate() function
    ani = animation.FuncAnimation(fig, animate, frames=len(x), \
                                      interval=interV, blit=True, repeat=True)
    ani.save(outpath)
    plt.show()
    
 
    

#Automatic find ROI bg color from 
def AutoROIbg(img):
    """
    Function to find ROI color from BW image:
        if ROI is 255, then the bg is 0
    """
    bg=int(np.mean(img))
    if bg<128:
        ROI =255
    else:
        ROI = 0
    return ROI
            