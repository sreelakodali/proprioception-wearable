
% Sreela Kodali, kodali@stanford.edu
% Reading Raw Data from Staircasing JND and plotting
% clear;
% close all;
clear;
N_SUBJECT = 12;

if (N_SUBJECT == 7)
% subject 7
dataDir = ["subject7_2025-02-12_20-53", "subject7_2025-02-12_21-17", "subject7_2025-02-12_22-02"];
nActArr = [2*ones(1,4), ones(1,4)]; % number of actuators for corresponding above directory
calibrationDir = 'subject7_2025-02-12_20-40';
coordinates = [1, 1, 1; 2, 1, 2; 3, 2, 1; 4, 2, 2; 5, 3, 1; 6, 3, 2; 7, 4, 1; 8, 4, 2]; % for subjects 6 and 7, nTrials=2
nTrials = 2;
indices = [45,263];
cellPlotOrder = [5, 6, 7, 8, 1, 2, 3, 4];

elseif (N_SUBJECT == 6)
% subject 6
dataDir = ["subject6_2025-02-12_10-42"];
nActArr = [ones(1,4), 2*ones(1,4)]; % number of actuators for corresponding above directory
calibrationDir = 'subject6_2025-02-12_10-42';
coordinates = [1, 1, 1; 2, 1, 2; 3, 2, 1; 4, 2, 2; 5, 3, 1; 6, 3, 2; 7, 4, 1; 8, 4, 2]; % for subjects 6  and 7, nTrials=2
nTrials = 2;
indices = [295, 443];
cellPlotOrder = [1, 2, 3, 4, 5, 6, 7, 8];

elseif (N_SUBJECT == 5)
% subject 5
dataDir = ["subject5_2025-02-11_16-12", "subject5_2025-02-11_17-17", "subject5_2025-02-11_17-32"];
nActArr = [2*ones(1,6), ones(1,4)]; % number of actuators for corresponding above directory
calibrationDir = 'subject5_2025-02-11_15-55';
coordinates = [1, 1, 1; 2, 1, 2; 4, 2, 1; 5, 2, 2; 7, 3, 1; 8, 3, 2; 9, 3, 3; 10, 4, 1; 11, 4, 2; 12, 4, 3]; % for subject 5, nTrials=3
nTrials = 3;
indices = [518,663];
%cellPlotOrder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
cellPlotOrder = [7, 8, 9, 10, 1, 2, 3, 4, 5, 6];
% 1, 2, 3 - 2q1
% 4, 5, 6 - 2q2
% 7, 8 - 1q1
% 9, 10 - 1q2

idxUser = 6; % which calibration strand plotted

elseif (N_SUBJECT == 8)
dataDir = ["subject8_2025-02-17_17-42"];
nActArr = [2*ones(1,4), ones(1,4)]; % number of actuators for corresponding above directory
calibrationDir = 'subject8_2025-02-17_17-42';
coordinates = [1, 1, 1; 2, 1, 2; 3, 2, 1; 4, 2, 2; 5, 3, 1; 6, 3, 2; 7, 4, 1; 8, 4, 2]; % for subjects 6  and 7, nTrials=2
nTrials = 2;
indices = [62,211];
%cellPlotOrder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
cellPlotOrder = [7, 8, 5, 6, 3, 4, 1, 2];

elseif (N_SUBJECT == 9)
dataDir = ["subject9_2025-02-18_18-36", "subject9_2025-02-18_19-49"];
nActArr = [ones(1,4), 2*ones(1,4)]; % number of actuators for corresponding above directory
calibrationDir = 'subject9_2025-02-18_18-25';
coordinates = [1, 1, 1; 2, 1, 2; 3, 2, 1; 4, 2, 2; 5, 3, 1; 6, 3, 2; 7, 4, 1; 8, 4, 2]; % for subjects 6  and 7, nTrials=2
nTrials = 2;
indices = [65,190];
%cellPlotOrder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
cellPlotOrder = [3, 4, 1, 2, 7, 8, 5, 6];

elseif (N_SUBJECT == 10)
dataDir = ["subject10_2025-02-19_10-46"];
nActArr = [ones(1,4), 2*ones(1,4)]; % number of actuators for corresponding above directory
calibrationDir = 'subject10_2025-02-19_10-46';
coordinates = [1, 1, 1; 2, 1, 2; 3, 2, 1; 4, 2, 2; 5, 3, 1; 6, 3, 2; 7, 4, 1; 8, 4, 2]; % for subjects 6  and 7, nTrials=2
nTrials = 2;
indices = [65,190];
%cellPlotOrder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
cellPlotOrder = [3, 4, 1, 2, 7, 8, 5, 6];

elseif (N_SUBJECT == 11)
% subject sk, test
dataDir = ["subject11_2025-04-01_20-45"];
nActArr = [ones(1,2)]; % number of actuators for corresponding above directory
calibrationDir = 'subject11_2025-04-01_20-45';
coordinates = [1, 1, 1; 2, 1, 2];
nTrials = 2;
indices = [65,190];
cellPlotOrder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

elseif (N_SUBJECT == 12)
% subject sk, test
dataDir = ["subject12_2025-04-02_14-22"];
nActArr = [ones(1,2)]; % number of actuators for corresponding above directory
calibrationDir = 'subject12_2025-04-02_14-22';
coordinates = [1, 1, 1; 2, 1, 2];
nTrials = 2;
indices = [65,190];
cellPlotOrder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

end

% plot each trial*.csv file
[subjectN, cellArr, yMax] = plotAllTrials(dataDir, nActArr, 1);


% plot all trials in grid format
[subjectN, JNDArr, JNDAbsArr] = plotAllTrialsGrid(subjectN, cellArr, cellPlotOrder, yMax, nTrials, coordinates);

% % plot calibration
% plotCalibration(subjectN, calibrationDir, indices);


if N_SUBJECT == 6
% specific modifications
JNDArr(4,1) = JNDArr(4,2);
JNDArr(3,1) = JNDArr(3,2);
avgJND = reshape(transpose(mean(JNDArr,2)), [2,2]);
tJNDArr = transpose(JNDArr);
stdErr = [(std(tJNDArr(:,1:2))/sqrt(2))' , (std(tJNDArr(:,3:4))/sqrt(1))'] ;



elseif N_SUBJECT == 5
A = mean(JNDArr(1:2,1:2),2);
B = mean(JNDArr(3:4,2:3),2);
avgJND = [A, B];
tJNDArr = transpose(JNDArr);
stdErr = [(std(tJNDArr(1:2,1:2))/sqrt(2))', (std(tJNDArr(:,3:4))/sqrt(3))'];
% A = mean(JNDArr(1:2,1:2),2);
% B = mean(JNDArr(3:4,2:3),2);
% avgJND = [A, B];
% stdErr = [(std(JNDArr(1:2,1:2))/sqrt(2))', (std(JNDArr(3:4,2:3))/sqrt(2))'];
% avgJND = reshape(mean(JNDArr,2), [2,2]);
% stdErr = reshape(std(JNDArr')/sqrt(2), [2,2]);


elseif ismember(N_SUBJECT, [7, 8, 9, 10, 11, 12])
avgJND = reshape(mean(JNDArr,2), [2,2]);
stdErr = reshape(std(JNDArr')/sqrt(2), [2,2]);

% 


% elseif subjectN == '8'
% avgJND = reshape(mean(JNDArr,2), [2,2]);
% 
% elseif subjectN == '9'
% avgJND = reshape(mean(JNDArr,2), [2,2]);


end


figure;
set(gcf,'color','white');
ax = gca(gcf);
b = bar(avgJND, 'EdgeColor','none'); hold on;
z = [b(1).XEndPoints',b(2).XEndPoints'];
er = errorbar(z, avgJND, stdErr, 'color', 'k', 'linestyle', 'none', 'linewidth', 1.5); hold on;
title(strcat("JND Results: Subject ", subjectN));
xlabel('Quartile');
ylabel('JND (N)');
ax.FontSize = 15;
leg = legend({'Single Contact', 'Two Contacts'}, 'Location','northwest', 'edgeColor','w');