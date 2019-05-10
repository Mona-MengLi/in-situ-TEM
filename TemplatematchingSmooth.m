%##########################################################################
%###########  Remove gittering in template matching results ###############
%################### by Meng Li 2019.03.09 ################################
%################### mona.mengli@gmail.com ################################
%##########################################################################
%=====================Input: ==============================================
%txt log file from Template matching like: 
%            Slice:330 X displacement:-1.0 Y displacement:0.0
%=====================Output:==============================================
% Translation matrix in form of [slice dx dy]
%==========================================================================


% %1. read result TXT file convert to formated csv
clc;
clear all;
close all;



w = 20; % input filtersize to median points
w2 =10; 
[name,path ] = uigetfile({'*.txt'});
fname=[path,name];
outname=[name(1:end-4),'_',num2str(w),'MF.csv'];
fout=[path,outname];
outname2=[name(1:end-4),'.csv'];
fout2=[path,outname2];
outname3=[outname(1:end-4),'_',num2str(w2),'SF.csv'];
fout3=[path,outname3];

Ori = fileread(fname);
Slice = 'Slice:';
Dx = 'X displacement:';
Dy = 'Y displacement:';
Str1 = strrep(Ori,Slice,'');
Str2 = strrep(Str1,Dx,' ');
Str3 = strrep(Str2,Dy,' ');
TM = str2num(Str3);%the extracted translation matrix

M = [0 0 0; TM];
if TM(1,1)==2
    M(1,1)= 1;
else
    M(1,1)= TM(1,1)+1;
end
n=length(M);
SliceEnd=n;
% SliceEnd=806;%Slice number to abort template matching result


% 2. calculate new translation needed
N = sortrows(M,1);
N(SliceEnd:end,2)=N(SliceEnd-1,2);
csvwrite(fout2,N);

% move median filtering to remove noise
D = N;
% size(D)

D(:,2)=[smoothdata(N(:,2)','movmedian',w)]';
D(:,3)=[smoothdata(N(:,3)','movmedian' ,w)]';
csvwrite(fout,D)


E = D;

E(:,2)=[smoothdata(D(:,2)','rlowess',w2)]';%methods: 'movmean' (default) | 'movmedian' | 'gaussian' | 'lowess' | 'loess' | 'rlowess' | 'rloess' | 'sgolay'
% E(:,2)=[smoothdata(E(:,2)','sgolay',w2)]';%Robust linear regression
E(:,3)=[smoothdata(D(:,3)','rlowess' ,w2)]';


csvwrite(fout3,E)

plot(N(:,1),N(:,2),'k',D(:,1),D(:,2),'b*',E(:,1),E(:,2),'ro-')
 figure;
 plot(N(:,1),N(:,3),'k',D(:,1),D(:,3),'b--',E(:,1),E(:,3),'ro')

