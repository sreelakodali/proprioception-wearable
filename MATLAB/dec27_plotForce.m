close all;

%file = '2024-12-27_05-32'; 
%file = '2024-12-27_07-25';
file = '2024-12-28_03-41';


path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/';
data = readmatrix(strcat(path,file, '/raw_', file,'.csv'),'NumHeaderLines',0);

%
time = data(:,1)/1000;
commandActuatorPos = data(:,2) * (27.0/4095);
measuredActuatorPos =  data(:,3) * (27.0/4095);
rawForceData = data(:,4); %(data(:,4) - 255) * 45/512;
matlablibraryFilteredData = data(:,5); %(data(:,5) - 255) * 45/512;
%iirFormFilteredData = data(:,6); %(data(:,6) - 255) * 45/512;


% figure;
% set(gcf,'color','white');
% gca(gcf);
% %plot(time(1:100,:), rawForceData(1:100,:), time(1:100,:), matlablibraryFilteredData(1:100,:));
% plot(time, rawForceData, time, matlablibraryFilteredData+10,  time, skFilter_fs32_fpass025(rawForceData)+20, time, skFilter_fs32_fpass035(rawForceData)+30, time, skFilter_fs32_fpass04(rawForceData)+40, time, skFilter_fs32_fpass05(rawForceData)+50, time, round(skFilterBands(rawForceData))+60);
% %ylim([0,13]);
% %xlim([0,50]);

w = 50;
coeffWindow = ones(1,w)/w;
filteredAVG = filter(coeffWindow, 1, rawForceData);
filteredMedian = medfilt1(rawForceData,w);

plotData = [rawForceData, matlablibraryFilteredData, skFilter_fs32_fpass025(rawForceData), skFilter_fs32_fpass035(rawForceData), skFilter_fs32_fpass04(rawForceData), skFilter_fs32_fpass05(rawForceData), filteredAVG, filteredMedian, skFilter_fs32_fpass65(rawForceData)];


figure;
set(gcf,'color','white');
gca(gcf);
for i = 1:size(plotData,2)
    plot(time, round(plotData(:,i)) + 10*(i-1)); hold on;
end
title("Force Data with Different Fc LPF");

% figure;
% set(gcf,'color','white');
% gca(gcf);
% plot(time, rawForceData); hold on;
% 
% % windowSizes = [10,20, 30, 40, 50];
% % for i = 1:size(windowSizes,2)
% %     coeffWindow = ones(1,windowSizes(i))/windowSizes(i);
% %     plot(time, filter(coeffWindow, 1, rawForceData) + 10 + 20*(i-1)); hold on;
% %     plot(time, medfilt1(rawForceData,windowSizes(i)) + 20 + 20*(i-1)); hold on;
% % end
% % title("Force Data with Both Moving Average and Median Filter");

figure;
set(gcf,'color','white');
gca(gcf);
plot(time, rawForceData); hold on;
windowSizes = 10:10:100;
for i = 1:size(windowSizes,2)
    coeffWindow = ones(1,windowSizes(i))/windowSizes(i);
    plot(time, filter(coeffWindow, 1, rawForceData) + 10 + 10*(i-1)); hold on;
end
title("Force Data with Moving Average");

figure;
set(gcf,'color','white');
gca(gcf);
plot(time, rawForceData); hold on;
windowSizes = 10:10:100;
for i = 1:size(windowSizes,2)
    plot(time, medfilt1(rawForceData,windowSizes(i)) + 20 + 20*(i-1)); hold on;
end
title("Force Data with Median Filter");

% windowSize = 1000;
% for i = 1:floor(length(time)/windowSize)
%     a = 1+(i-1)*windowSize;
%     b = windowSize*i; 
%    figure;
%    set(gcf,'color','white');
%    gca(gcf);
%    %plot(time(a:b,:), commandActuatorPos(a:b,:), time(a:b,:), measuredActuatorPos(a:b,:)); hold on;
%    plot(time(a:b,:), rawForceData(a:b,:), time(a:b,:), matlablibraryFilteredData(a:b,:)+10, time(a:b,:), skFilter_fs32_fpass025(rawForceData(a:b,:))+20, time(a:b,:), skFilter_fs32_fpass035(rawForceData(a:b,:))+30, time(a:b,:), skFilter_fs32_fpass04(rawForceData(a:b,:))+40, time(a:b,:), skFilter_fs32_fpass05(rawForceData(a:b,:))+50, time(a:b,:), round(skFilterBands(rawForceData(a:b,:)))+60);%time(a:b,:), iirFormFilteredData(a:b,:)+20);
% 
% end