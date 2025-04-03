clear;
close all;


% CALIBRATION
% checking update to reversal algorithm
% dataDir = ["subjectsk_2025-02-06_18-39", "subjectsk_2025-02-06_18-50", "subjectsk_2025-02-17_03-46"];
% nActArr = [ones(1,5)];
% [subjectN, cellArr, yMax] = plotAllTrials(dataDir, nActArr, 1);

subjectN8 = '8';
calibrationDir8 = 'subject8_2025-02-17_17-42';
indices8 = [62,211];

subjectN7 = '7';
calibrationDir7 = 'subject7_2025-02-12_20-40';
indices7 = [72,169];

subjectN6 = '6';
calibrationDir6 = 'subject6_2025-02-12_10-42';
indices6 = [295, 443];

subjectN5 = '5';
calibrationDir5 = 'subject5_2025-02-11_15-55';
indices5 = [518,663];

subjectN4 = '4';
calibrationDir4 = 'subject4_2025-01-31_18-16';
indices4 = [110,223];

subjectN3 = '3';
calibrationDir3 = 'subject3_2025-01-30_20-23';
indices3 = [76,260];

subjectN2 = '2';
calibrationDir2 = 'subject2_2025-01-30_15-00';
indices2 = [67,198];


% plot calibration
[dist2, force2, p2] = plotCalibration(subjectN2, calibrationDir2, indices2);
[dist3, force3, p3] = plotCalibration(subjectN3, calibrationDir3, indices3);
[dist4, force4, p4] = plotCalibration(subjectN4, calibrationDir4, indices4);
[dist5, force5, p5] = plotCalibration(subjectN5, calibrationDir5, indices5);
[dist6, force6, p6] = plotCalibration(subjectN6, calibrationDir6, indices6);
[dist7, force7, p7] = plotCalibration(subjectN7, calibrationDir7, indices7);
[dist8, force8, p8] = plotCalibration(subjectN8, calibrationDir8, indices8);

distCell = {dist2, dist3, dist4, dist5, dist6, dist7, dist8};
forceCell = {force2, force3, force4, force5, force6, force7, force8};
pCell = {p2(1,1), p3(1,1), p4(1,1),p5(1,1),p6(1,1),p7(1,1), p8(1,1)};