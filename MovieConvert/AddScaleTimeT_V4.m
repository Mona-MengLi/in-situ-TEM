%##########################################################################
%######## Moive add scale bar,timestamp,Temperature and Accelerate ########
%################### by Mona Li 2019.02.22 ################################
%################### mona.mengli@gmail.com ################################
%##########################################################################
%==========V2: added temperature data, gui select and TIFF support=========
%==========V4: 20190315 add function to simplify=======================

clc;

%========================================
% 1. initiation settings


    
token = input('Do you want to use the previous settings? 1-Yes, 0-No:  ');

if token ==0
    clear all, close all;
    
    %========================================
    % 2. Get info from the input movie file
    disp('######################################################')
    disp('1. Get initiation parameters of the input movie');
    disp('   ')
    [moviein,path ] = uigetfile({'*.tif;*.mp4'},'Select Movie/Tif stack to output:  ');
    str=moviein(end-3:end);
    if strcmp(str,'.tif')
        filetype = 2;
    else
        filetype =1;
    end
    
    if(path==0)
        return;
    end
    fname = [path,moviein];
    
    [fr1,fpsin,nFrames,W,H]=readTifMov(fname,filetype);
%     W=W/3;%For RGB image
    sf_in=input('Input speed factor of the input movie:    ');
    
    
    disp('######################################################')
    disp('2. Get parameters for the output movie')
    disp('   ')
    fpsout=input('Input fps of the output movie:(default=25)    ');
    if (fpsout == 0)
        disp('Error output fps input!')
        return;
    end
    movieout=[moviein(1:end-4),'_'];
    
    
    %========================================
    % 3. Function selections and initiaton
    
    disp('######################################################')
    disp('3.Function selections')
    disp('   ')
    
    % 3.1 Acc
    disp('================================================')
    sf_out=input('Input speed factor of the output movie:(default=fps_out/fps_in) ');
    if sf_out<1
        disp('Wrong sf_out input!')
        return
    elseif sf_out > 1
        movieout=[movieout,'X', num2str(sf_out)] ; %output movie name
    end
    %get scaled frame index
    In=zeros(nFrames,1);
    for i=1:nFrames
        In(i)=i;
    end
    Out=ScaleArray(In,sf_out,fpsin,fpsout);
    nFramesOut=length(Out);
    
    
    %3.2 Scale bar
    disp('================================================')
    IfScale=input('Do you need to add scalebar? 1-Yes, 0-No: ');
    if IfScale==1
        movieout=[movieout,'Sc'] ;
        disp('----------------------')
        dLength=input('Input desired scale bar length(nm):'); %input desired scale bar length:nm
        [pixscale x y]=getscalebar(dLength);%Get scale bar info
    end
    
    
    %3.3 timestamp
    disp('================================================')
    IfTime=input('Do you need to add timestampe? 1-Yes, 0-No: ');
    if IfTime == 1
        disp('----------------------')
        starttime=input('Input starttime of the input movie (s):   ');%start  time of the input movie: s
        disp('----------------------')
        style = input('Select timestamp style: 1- HH:MM:SS; 2-ss.s:  ');
        Timestamp=creatTimeStamp(nFrames,sf_in,fpsin,starttime,style);
        movieout=[movieout,'t'] ;
    end
    
    
    %3.4 Temperature
    disp('================================================')
    IfTemp=input('Do you need to add temperature? 1-Yes, 0-No: ');
    if IfTemp == 1
        disp('----------------------')
        HRate = input('Input heating rate (C/min):   ');
        
        T0 = input('Input starting temperature(C):  ');
        if HRate == 0
            T1 = T0;
            holdtime =0;
        else
            T1 = input('Input ending temperature(C):  ');
            holdtime=input('Input holdtime before temperature applied in the original(unaccelerated) movie (s):   ');%start  time of the input movie: s
        end
        
        Temp=creatTempArray(nFrames,sf_in,fpsin,HRate,T0,T1,holdtime);
        movieout=[movieout,'T'] ;
        
    end
    
    fout = [path,movieout];
else
    disp('Use previous settings!')
end


%========================================
% 4. Test output
disp('######################################################')
disp('4.Test output')
disp('   ')
% input parameters for the texts
fontsize_sc=20; %font size for scale bar
fontsize_t=20; %font size for timestamp
color='w';%
% color='k';
if color == 'w'
    color_boarder = 'k';
else
    color_boarder ='w';
end
 %text aligned 50px from lower left corner
w4=20;
%positon for scalebar
if IfScale ==1 
    Scalebar=[num2str(dLength),' nm'];
    h4=H-w4;
    xSc=x+w4; %size for scale bar x
    ySc=y+h4; %size for scale bar y
    %Position for scale bar: left bottom corner
    xS=w4;
    yS=h4-15;
    Ps=[xS,yS];
    Scale=[xSc;ySc];
else
        Ps=[0 0];
    Scale=[0 0];
    dLength=0;
end

%position of timestamp
if IfTime == 1
    % xt=w3-145;
    xt=W-20;
    % yt=w4;
    yt=H-w4-10;
    Pt=[xt,yt];
    if style == 1
        time=[num2str(Timestamp(1,2),'%02.0f') ':' num2str(Timestamp(1,3),'%02.0f') ':' num2str(Timestamp(1,2),'%02.0f')]; % HH:mm:SS
        
    elseif style ==2
        time=[num2str(Timestamp(1,2),'%02.1f') ' s']; % if SS.s s
        
    end
else
    Pt=[0 0];
    time = 0;
end

%position for Temperature
if IfTemp == 1
    xT=W-20;
    yT=w4;
    PT=[xT,yT];
     temp = [num2str(Temp(1,2),'%.0f') ' C'];
else
    PT=[0 0];
    temp = 0;
end 

%test ouput
frOut=AddStT2img(fr1,IfScale,IfTime,IfTemp,Ps,Pt,PT,dLength,Scale,time,temp,color,color_boarder,fontsize_sc,fontsize_t);
imshow(frOut)
key=input('Press 1 if you are satisfied with the positions:  ');
if key~=1
    disp('Aborted! Modify positions and retry~')
    return
end


%===========================================================
% 5. Output
outMov = struct('cdata',zeros(H,W,3,'uint8'),...
    'colormap',[]);


disp('######################################################')
disp('Movie output started!')
%initializing video writing
writerObj = VideoWriter(fout,'MPEG-4'); %select the following compression modes:
writerObj.FrameRate=fpsout;
writerObj.Quality=100;
disp('######################################################')
disp('Video settings are:')
writerObj
open(writerObj);

disp('######################################################')
disp('Percent    Frame/Total')


for k=1:nFramesOut
    if filetype==1
        fr = read(fname,Out(k));
    elseif filetype==2
        fr = imread(fname,Out(k));
    end
    if IfTemp == 1
        temp = [num2str(Temp(k,2),'%.0f') ' C'];
    end
    if IfTime == 1
        if style == 1
            time=[num2str(Timestamp(k,2),'%02.0f') ':' num2str(Timestamp(k,3),'%02.0f') ':' num2str(Timestamp(k,2),'%02.0f')]; % HH:mm:SS
            
        elseif style ==2
            time=[num2str(Timestamp(k,2),'%02.1f') ' s']; % if SS.s s

        end
    end
            

    outMov(k).cdata=AddStT2img(fr,IfScale,IfTime,IfTemp,Ps,Pt,PT,dLength,Scale,time,temp,color,color_boarder,fontsize_sc,fontsize_t);

    writeVideo(writerObj,outMov(k).cdata);

    completion=k/nFramesOut;
    display([num2str(completion*100,3) '         ' num2str(k) '/' num2str(nFramesOut)])

end
close(writerObj);
close all;
display('######################################################')
display('DONE! Enjoy~')
display('Have a nice day~ :)')
display('######################################################')


