% Sreela Kodali, kodali@stanford.edu
% Reading Raw Data from Staircasing JND and plotting
% SPECIFICALLY, HARDWARE PERFORMANCE
% clear;
% close all;
clear;
close all;

dataDir = ["subject12_2025-04-02_14-22"];%"subject8_2025-02-17_17-42" #subjectsk_2025-03-28_18-11
% nActArr = [2*ones(1,4), ones(1,4)]; % number of actuators for corresponding above directory
% calibrationDir = 'subject8_2025-02-17_17-42';
% coordinates = [1, 1, 1; 2, 1, 2; 3, 2, 1; 4, 2, 2; 5, 3, 1; 6, 3, 2; 7, 4, 1; 8, 4, 2]; % for subjects 6  and 7, nTrials=2
% nTrials = 2;
% indices = [62,211];
% %cellPlotOrder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
% cellPlotOrder = [7, 8, 5, 6, 3, 4, 1, 2];

path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/';
%fileName1 = 'raw_' + dataDir(1) +'.csv';
fileName1 = 'EXP_processed_device1_' + dataDir(1) +'.csv';
%fileName2 = 'EXP_processed_device2_' + dataDir(1) +'.csv';
device1Data = readmatrix(strcat(path,dataDir,'/',fileName1));
%device2Data = readmatrix(strcat(path,dataDir,'/',fileName2));
device1Data = device1Data(600:end,:);

t1 = device1Data(:,1)/1000;
t1 = t1 - t1(1);
command1= device1Data(:,2);
force1 = device1Data(:,3);

stimulusLength = 104;

idx = find(diff(command1) < 0); %find(ischange(command1));
idxS = idx-stimulusLength;

%idx1 = idx(2)-5;
idx1 = 1;
idx2 = idx(end)+20;
% idx1 = idx(1)-20;
% idx2 = idx(256)+20;
figure;
set(gcf,'color','white');
ax = gca(gcf);
plot(t1(idx1:idx2), command1(idx1:idx2), 'LineWidth',1.2); hold on;
plot(t1(idx1:idx2), force1(idx1:idx2), 'LineWidth',1.2); hold on;
scatter(t1(idx), command1(idx), 'cyan', 'filled'); hold on;
%scatter(t1(idxS), command1(idxS), 'cyan', 'filled'); hold on;
ax.FontSize = 18;
ylim([0,max(force1)]);
xlabel("time (s)")
ylabel("force (N)")


% generate dictionary for dataset
d = {};
commandKeys = [command1(idx), idx];
sortedcommandKeys = sortrows(commandKeys, 1);

i = 1;
while i <= size(sortedcommandKeys,1)
    k = sortedcommandKeys(i,1);
    occurances = find(sortedcommandKeys(:,1)==k);

    c = [];
    for j = 1:length(occurances)
        newValues = [(sortedcommandKeys(occurances(j), 2)-stimulusLength):sortedcommandKeys(occurances(j), 2)];
        c = [c, newValues];
    end
    d{end+1} = c;
    i = i + length(occurances);
end
d = transpose(d);
dict = dictionary(unique(sortedcommandKeys(:,1)),d);

allKeys = keys(dict);
meanVals = [];
stdErr = [];
grad = [];
for i = 1:length(allKeys)
    disp(allKeys(i));
    %disp(cell2mat(dict(allKeys(i))));
    v = force1(cell2mat(dict(allKeys(i))));
    meanVals(end+1) = mean(v);
    stdErr(end+1) = std(v)/sqrt(length(v));
    grad(end+1) = sum(abs(diff(v)));
    %disp(mean(force1(cell2mat(dict(allKeys(i))))));
end

figure;
set(gcf,'color','white');
ax = gca(gcf);
b = bar([allKeys, transpose(meanVals)]); hold on;
z = b(2).XEndPoints;
errorbar(z, meanVals, stdErr, 'color', 'k', 'linestyle', 'none', 'linewidth', 1.2); hold on;
%scatter(allKeys,meanVals, 'filled', 'red');
ax.FontSize = 18;
ylim([0,max(force1)]);
xlabel("# of Distinct Force Commands")
ylabel("Force (N)")
leg = legend('Commanded Force','Measured Force');
set(leg, 'edgeColor','w', 'Location','northwest');


figure;
set(gcf,'color','white');
ax = gca(gcf);
%bar([allKeys, transpose(meanVals)]);
plot(2:max(force1), 2:max(force1), 'LineWidth',1.0, 'Color','k', 'LineStyle','--'); hold on;
%scatter(allKeys,meanVals,'filled','r'); hold on;
plot(allKeys,meanVals, 'Marker','o', 'MarkerEdgeColor','r', 'MarkerFaceColor','r', 'LineStyle','none', 'MarkerSize',8); hold on;
errorbar(allKeys, meanVals, stdErr, 'color', 'k', 'linestyle', 'none', 'linewidth', 1.2); hold on;

ax.FontSize = 18;
xlim([2,max(force1)]);
ylim([2,max(force1)]);
xlabel("Commanded Forces (N)")
ylabel("Measured Force (N)")