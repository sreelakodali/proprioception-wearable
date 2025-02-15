%close all;

%file = '2024-12-27_05-32'; 
%file = '2024-12-27_07-25';
%file = '2024-12-28_03-41';
% file = '2024-12-29_01-10';
%file = '2024-12-29_03-30';
%file = '2025-01-04_21-32';
%file = '2025-01-05_00-13';
%file = '2025-01-05_00-18';
%file = '2025-01-05_00-58';
%file = '2025-01-05_02-44';
file = '2025-01-08_08-23';
%file = '2025-01-08_19-00'
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/';
data = readmatrix(strcat(path,file, '/raw_', file,'.csv'),'NumHeaderLines',0);
color2 = "#37BEB0";%staircase
color3 = "#0C6170"; %JND

% color3 = "#FB6090";%staircase
% color2 = "#821D30"; %JND

fileArr = ["2024-12-29_03-30", "2025-01-04_21-32", "2025-01-05_00-13", "2025-01-05_00-58", "2025-01-05_01-21", "2025-01-05_02-10", "2025-01-05_02-17", "2025-01-05_02-27", "2025-01-05_02-32", "2025-01-05_02-44", "2025-01-05_03-33", "2025-01-05_03-38"];
%
% 
% for j = 1:size(fileArr,2)
%     f = fileArr(j);
%     d = readmatrix(strcat(path,f, '/raw_', f,'.csv'),'NumHeaderLines',0);
%     t = d(:,1)/1000;
%     s = d(:,2);
%     fo = d(:,3);
%     c = d(:,5);
% 
%     figure;
%     set(gcf,'color','white');
%     gca(gcf);
%     plot(t, s); hold on;
%     plot(t,fo); hold on;
%     title(f);
% 
% end
time = data(:,1)/1000;
setpoints = data(:,2);
filteredForce = data(:,3);

% filteredForce(filteredForce<0.8)=0;
% endpieceFilteredForce = filteredForce(3000:end,:);
% endpieceFilteredForce(endpieceFilteredForce<1.5)=0;
% filteredForce(3000:end,:) =endpieceFilteredForce;
rawFilteredForce = data(:,4);
commandActuatorPos = data(:,5);
measuredActuatorPos = data(:,6);

plotData3 = [setpoints, filteredForce];
% figure;
% set(gcf,'color','white');
% ax = gca(gcf);
% 
% for i = 1:size(plotData3,2)
%     plot(time, plotData3(:,i)); hold on;
% end
% title("Force vs Time for Different Force Setpoints");
% xlabel('Time (s)')
% ylabel('Force (N)')
% ax.FontSize = 15;
% ylim([0,25]);
% 
% % yyaxis right
% % ylabel("Actuator Position (mm)")
% % % ylim([0,10])
% % plot(time, measuredActuatorPos * 27.0/4095); hold on;
% 
% leg = legend('Setpoint Command', 'Measured Force');
% set(leg, 'edgeColor','w', 'Location','northeast');


timediffdataArr = ["2025-01-08_08-23", "2025-01-08_19-00"];

data1 = readmatrix(strcat(path,timediffdataArr(1,1), '/raw_', timediffdataArr(1,1),'.csv'),'NumHeaderLines',0);
data2 = readmatrix(strcat(path,timediffdataArr(1,2), '/raw_', timediffdataArr(1,2),'.csv'),'NumHeaderLines',0);

time1 = data1(:,1)/1000;
setpoints1 = data1(:,2);
filteredForce1 = data1(:,3);

time2 = data2(:,1)/1000;
setpoints2 = data2(:,2);
filteredForce2 = data2(:,3);

lw = 2;
figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);
ax.FontSize = 15;

s1 = subplot(2,1,1);

% xlim([1,50])
 plot(time1-28.5, setpoints1, 'LineWidth',lw, 'Color', color2); hold on;
 plot(time1-28.5, filteredForce1, 'LineWidth',lw, 'Color', color3); hold on;
xlabel('Time (s)')
ylabel('Force (N)')
ylim([0,24]);
xlim([0,140]);
s1.FontSize = 15;
leg = legend('Setpoint Command', 'Measured Force');
set(leg, 'edgeColor','w', 'Location','northwest');
t1 = title("Fixed Time for Force Commands");
%t1.FontWeight = 'normal';
s2 = subplot(2,1,2);

plot(time2-38, setpoints2, 'LineWidth',lw, 'Color', color2); hold on;
 plot(time2-38, filteredForce2, 'LineWidth',lw, 'Color', color3); hold on;
xlabel('Time (s)')
ylabel('Force (N)')
ylim([0,24]);
xlim([0,140]);
s2.FontSize = 15;
% bigTitle= sgtitle("Force vs Time for Various Setpoints");
% bigTitle.FontSize = 20;
% bigTitle.FontWeight = 'bold';
t2 = title("Fixed Time for Measured Force");
%t2.FontWeight = 'normal';


% % commandActuatorPos = data(:,2) * (27.0/4095);
% % measuredActuatorPos =  data(:,3) * (27.0/4095);
% % rawForceData = data(:,4); %(data(:,4) - 255) * 45/512;
% % matlablibraryFilteredData = data(:,5); %(data(:,5) - 255) * 45/512;
% % %iirFormFilteredData = data(:,6); %(data(:,6) - 255) * 45/512;
% % 
% % matlab2libraryFilteredData = data(:,6);
% % movingAvgFilteredData = data(:,7);
% % iirFilteredData = data(:,8);
% % medFilteredData = data(:,9);
% 
% % figure;
% % set(gcf,'color','white');
% % gca(gcf);
% % %plot(time(1:100,:), rawForceData(1:100,:), time(1:100,:), matlablibraryFilteredData(1:100,:));
% % plot(time, rawForceData, time, matlablibraryFilteredData+10,  time, skFilter_fs32_fpass025(rawForceData)+20, time, skFilter_fs32_fpass035(rawForceData)+30, time, skFilter_fs32_fpass04(rawForceData)+40, time, skFilter_fs32_fpass05(rawForceData)+50, time, round(skFilterBands(rawForceData))+60);
% % %ylim([0,13]);
% % %xlim([0,50]);
% 
% w = 50;
% coeffWindow = ones(1,w)/w;
% filteredAVG = filter(coeffWindow, 1, rawForceData);
% filteredMedian = medfilt1(rawForceData,w);
% 
% plotData = [rawForceData, matlablibraryFilteredData, skFilter_fs32_fpass025(rawForceData), skFilter_fs32_fpass035(rawForceData), skFilter_fs32_fpass04(rawForceData), skFilter_fs32_fpass05(rawForceData), filteredAVG, filteredMedian, skFilter_fs32_fpass65(rawForceData)];
% 
% plotData2 = [rawForceData, matlablibraryFilteredData, matlab2libraryFilteredData, movingAvgFilteredData, iirFilteredData, medFilteredData];
% 
% figure;
% set(gcf,'color','white');
% gca(gcf);
% for i = 1:size(plotData2,2)
%     %plot(time, round(plotData(:,i)) + 10*(i-1)); hold on;
%     plot(time, round(plotData2(:,i))); hold on;
% end
% %title("Force Data with Different Fc LPF");
% plot(time, skFilterBS(rawForceData) + 35 ); hold on;
% plot(time, skFilterBS2(rawForceData) + 45 ); hold on
% title("Force Data with Different Filters");
% 
% 
% % figure;
% % set(gcf,'color','white');
% % gca(gcf);
% % plot(time, rawForceData); hold on;
% % 
% % % windowSizes = [10,20, 30, 40, 50];
% % % for i = 1:size(windowSizes,2)
% % %     coeffWindow = ones(1,windowSizes(i))/windowSizes(i);
% % %     plot(time, filter(coeffWindow, 1, rawForceData) + 10 + 20*(i-1)); hold on;
% % %     plot(time, medfilt1(rawForceData,windowSizes(i)) + 20 + 20*(i-1)); hold on;
% % % end
% % % title("Force Data with Both Moving Average and Median Filter");
% 
% % figure;
% % set(gcf,'color','white');
% % gca(gcf);
% % plot(time, rawForceData); hold on;
% % windowSizes = 10:10:100;
% % for i = 1:size(windowSizes,2)
% %     coeffWindow = ones(1,windowSizes(i))/windowSizes(i);
% %     plot(time, filter(coeffWindow, 1, rawForceData) + 10 + 10*(i-1)); hold on;
% % end
% % title("Force Data with Moving Average");
% % 
% % figure;
% % set(gcf,'color','white');
% % gca(gcf);
% % plot(time, rawForceData); hold on;
% % windowSizes = 10:10:100;
% % for i = 1:size(windowSizes,2)
% %     plot(time, medfilt1(rawForceData,windowSizes(i)) + 20 + 20*(i-1)); hold on;
% % end
% % title("Force Data with Median Filter");
% % 
% % % windowSize = 1000;
% % % for i = 1:floor(length(time)/windowSize)
% % %     a = 1+(i-1)*windowSize;
% % %     b = windowSize*i; 
% % %    figure;
% % %    set(gcf,'color','white');
% % %    gca(gcf);
% % %    %plot(time(a:b,:), commandActuatorPos(a:b,:), time(a:b,:), measuredActuatorPos(a:b,:)); hold on;
% % %    plot(time(a:b,:), rawForceData(a:b,:), time(a:b,:), matlablibraryFilteredData(a:b,:)+10, time(a:b,:), skFilter_fs32_fpass025(rawForceData(a:b,:))+20, time(a:b,:), skFilter_fs32_fpass035(rawForceData(a:b,:))+30, time(a:b,:), skFilter_fs32_fpass04(rawForceData(a:b,:))+40, time(a:b,:), skFilter_fs32_fpass05(rawForceData(a:b,:))+50, time(a:b,:), round(skFilterBands(rawForceData(a:b,:)))+60);%time(a:b,:), iirFormFilteredData(a:b,:)+20);
% % % 
% % % end