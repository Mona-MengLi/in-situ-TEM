    
function [scale x y]=getscalebar(dLength)
%function to get scale and scale bar coordinates for input dLength :nm

disp('----------------------')
        sb=input('Input scale bar(px/nm)[Ref: 700 kX-34.5?1000 kX-49.5], otherwise input 0:  ');
    if sb == 0 %get scale bar from movie
        
        disp('Select scalebar movie');
        [ movieScale,path2 ] = uigetfile({'*.mov;*.avi;*.mp4'});% scale bar movie
        fScale = [path2,movieScale];
        display('Read scale bar from movie')
        display('Select the scale bar area and right-click "Crop Image"!')
        movs = VideoReader(fScale);
        fr1=readFrame(movs);
        
        choice=input('Select method to get scale bar: 1-from ROI, 2-fixed area:    ');
        if choice==1
            imshow(fr1)
            [I2,rect] =imcrop;%returns the cropping rectangle in rect, rect=[x1, y1, x2,y2]
            rect
            [w,h]=size(I2); %gets the width and height of the new movie
        elseif choice ==2
            rect=[1165 0 157 25];%for H9500 : [1165 0 157 25]
        else
            return
        end
        
        %Show the croped area
        I3=imcrop(fr1,rect);
        
        [h,w]=size(I3); %gets the width and height of the new movie
        
        display('View the scale bar area')
        figure, imshow(I3), title('View the scale bar area');
        
        ActLength=input('Input scale bar length(nm):'); %Detect real length
%         dLength=input('Input desired scale bar length(nm):'); %input desired scale bar length:nm
        
        % [I4,rec2] =imcrop;
        % rec2
        I4=imcrop(I3,[0 15 w h]);
        % I4=imcrop(I3,[0 20 w h]) ;%get only the scale bar
        I5=im2bw(I4,0.5);
        figure, imshow(I5), title('View the scale bar');
        
        [h2,w2]=size(I5);
        pxLength=w2-sum(I5(5,:)); % get the pixel length
        
        scale=pxLength/ActLength %scale: px/nm
    else
        scale=sb;
%         dLength=input('Input desired scale bar length(nm):'); %input desired scale bar length:nm
    end
    DpxLength=scale*dLength; %desired px length
    
    x=[0,0,DpxLength,DpxLength];% x:x1,x2,x3,x4
    y=[0,10,10,0];% y:y1,..y4
    
end