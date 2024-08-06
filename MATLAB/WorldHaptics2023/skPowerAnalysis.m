% Power Analysis

close all

nHnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/avgnHnV_pythonGenerated_16.csv','NumHeaderLines',0);
nHV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/avgnHV_pythonGenerated_16.csv','NumHeaderLines',0);
HnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/avgHnV_pythonGenerated_16.csv','NumHeaderLines',0);
HV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/avgHV_pythonGenerated_16.csv','NumHeaderLines',0);

errorNotAbs = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/error_notABS.csv','NumHeaderLines',0);
 
nHnV = nHnV(:,4);
nHV = nHV(:,4);
HnV = HnV(:,4);
HV = HV(:,4);

w=4;

% HV = HV([1:w], :);
% nHnV = nHnV([1:w], :);
% nHV = nHV([1:w], :);
% HnV = HnV([1:w], :);


HV([2, 8], :) = [];
nHnV([2, 8], :) = [];
nHV([2, 8], :) = [];
HnV([2, 8], :) = [];

mean_nHnV = mean(nHnV);
mean_nHV = mean(nHV);
mean_HnV = mean(HnV);
mean_HV = mean(HV);

p0 = [mean(nHnV), std(nHnV)];
p1 = [mean(HnV)];

nout = sampsizepwr('t', p0, p1)
nout2 = sampsizepwr('t', p0, p1, 0.8)
pwrout = sampsizepwr('t', p0, p1, [], length(HV))



