%##########################################################################
%#############  Apply translation file to tif movie stack##################
%################### by Meng Li 2019.03.06 ################################
%################### mona.mengli@gmail.com ################################
%##########################################################################
%=====================Input: ==============================================
%1. translation file: csv, row 1: slice#(1-n),row 2:Dx(px), row 3:Dy(px) 
%2. tif stack to apply translation
%=====================Output:==============================================
%translated tif stack
%==========================================================================

%1.Read translate matrix
clc;clear all; close all;
[name,path] = uigetfile('*.csv','Select translation coordinate file','MultiSelect','on');
size(name);
type= class(name);

% [n l]=size(name);
if type == 'char'
    fname=[path,name];
   TM = csvread(fname);
%    size(TM) 
else
    n=length(name);

%     fname=[path,char(name(1))];
    TM = csvread([path,char(name(1))]);
    for i=2:n
%        fname=[path,char(name(i))];

        T = csvread([path,char(name(i))]);
        TM(:,2:3) = TM(:,2:3)+T(:,2:3);
    end
end



% 2. Apply translation matrix to the image stacks
[moviein,path ] = uigetfile({'*.tif'},'Select image stacks to apply shift');
movname=[path,moviein];
outmov=[moviein(1:end-4),'_TF.tif'];
outname=[path,outmov];
info = imfinfo(movname);
nFrames = numel(info);
disp('Start appling shift to images~')


for k=1:nFrames
    fr=imread(movname,k);
    fr2=imtranslate(fr,[TM(k,2),TM(k,3)],'FillValues',150);%fill with grey background
    if k==1
        imwrite(fr2,outname)
    else
        imwrite(fr2,outname,'WriteMode','append')
    end
    completion=k/nFrames;
    disp([num2str(completion*100,3) '%         ' num2str(k) '/' num2str(nFrames,4)])
end
disp('Conversion finished! Enjoy~')

