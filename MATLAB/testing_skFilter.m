%clear;
%close all;


file = '2024-07-16_20-35'; % without rigid
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/additionalData/';
data = readmatrix(strcat(path,file, '/raw_', file,'.csv'),'NumHeaderLines',0);
time = data(:,1)/1000;
rawCommand = data(:,2);
command = interp1([47, 139],[0, 20],data(:,2));
measured = interp1([986, 28],[0, 20],data(:,3));
force = data(:,4);



filteredHd2 = round(skFilter(int16(force)));