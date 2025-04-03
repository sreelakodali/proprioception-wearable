
% Sreela Kodali, kodali@stanford.edu
% Reading Raw Data from Staircasing JND and plotting

function [subjectN, JNDArr, JNDAbsArr, cellArr] = plotSubject_Staircasing(dataDir, nActArr, p, calibrationDir)
close all;


cellPlotOrder = [1, 2, 3, 4, 5, 6, 7, 8]; % 6, which order of data plotted
idxUser = 4; % which calibration strand plotted
nTrials = 2;
coordinates = [1, 1, 1; 2, 1, 2; 3, 2, 1; 4, 2, 2; 5, 3, 1; 6, 3, 2; 7, 4, 1; 8, 4, 2]; % for subjects 6 and 7, nTrials=2

% coordinates = [1, 1, 1; 2, 1, 2; 3, 1, 3; 4, 2, 1; 5, 2, 2; 6, 2, 3; 7,
% 3, 1; 8, 3, 2; 9, 4, 1; 10, 4, 2]; % for subject 5, nTrials=3


% plot each trial*.csv file
[subjectN, cellArr, yMax] = plotAllTrials(dataDir, nActArr, p);

nSubject = str2num(subjectN);

if nSubject == 5
    coordinates = [1, 1, 1; 2, 1, 2; 3, 1, 3; 4, 2, 1; 5, 2, 2; 6, 2, 3; 7, 3, 1; 8, 3, 2; 9, 4, 1; 10, 4, 2]; % for subject 6, nTrials=3
    nTrials = 3;
    cellPlotOrder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    idxUser = 6; % which calibration strand plotted
elseif nSubject ==7
    coordinates = [1, 1, 1; 2, 1, 2; 3, 2, 1; 4, 2, 2; 5, 3, 1; 6, 3, 2; 7, 4, 1; 8, 4, 2]; % for subjects 6 and 7, nTrials=2
    nTrials = 2;
    cellPlotOrder = [5, 7, 6, 8, 1, 2, 3, 4];

elseif nSubject ==6
    coordinates = [1, 1, 1; 2, 1, 2; 3, 2, 1; 4, 2, 2; 5, 3, 1; 6, 3, 2; 7, 4, 1; 8, 4, 2]; % for subjects 6  and 7, nTrials=2
    nTrials = 2;
    cellPlotOrder = [1, 2, 3, 4, 5, 6, 7, 8];
end



% plot all trials in grid format
[subjectN, JNDArr, JNDAbsArr] = plotAllTrialsGrid(subjectN, cellArr, cellPlotOrder, yMax, nTrials, coordinates);

% plot calibration
plotCalibration(subjectN, calibrationDir, idxUser);


end