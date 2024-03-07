% Plots for Haptics Symposium Work-in-Progress Paper 2024
% Written by Sreela Kodali kodali@stanford.edu

close all
twoPoke = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/forceOfStairCase_twoPoke_2024-01-30_20-21.csv','NumHeaderLines',1);
onePoke = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/forceOfStairCase_onePoke_2024-01-30_20-47.csv','NumHeaderLines',1);

nTrials = twoPoke(:,1);
twoPokeTest = twoPoke(:,2);
twoPokeTestMM = twoPoke(:,3);
onePokeTest = onePoke(:,2);
onePokeTestMM = onePoke(:,3);

idx_twoPokeReversals = [9, 11, 14, 16, 19, 23, 27, 29, 32, 34, 37, 39, 42, 44, 47, 49];
idx_onePokeReversals = [9, 11, 13, 15, 17, 19, 22, 24, 26, 28, 30, 32, 37, 39, 41, 43];

twoPokeReversalMask = zeros(50,1);
onePokeReversalMask = zeros(50,1);

twoPokeReversalMask(idx_twoPokeReversals) = 1;
onePokeReversalMask(idx_onePokeReversals) = 1;

twoPokeReversal = twoPokeReversalMask .* twoPokeTestMM;
onePokeReversal = onePokeReversalMask .* onePokeTestMM;



% map command to actuator position

noStdev = zeros(size(twoPokeTest));


color="#0C1446";%reversal
color2 = "#29A0B1";%staircase
color3 = "#FF2101"; %JND
color4 = "#190204"; %reference

% color = "#4F3F1F";%reversal
% color2="#499FA4";%staircase
% color3 = "#FE640C"; %JND
% color4 = "#000000"; %reference

% color = "#B00000";%reversal
% color2="#000000";%staircase
% color3 = "#FF2101"; %JND
% color4 = "#000000"; %reference
j = 1;
sz = 5;
lw2 = 2;
lw1 = 1;

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

%p = plot(nTrials, twoPokeTestMM, '-o', 'LineWidth',lw2, 'Color', color2, 'MarkerSize', 5, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2); hold on;

plotSK_JND(nTrials,twoPokeTestMM, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
%yline(95,'-k','LineWidth',lw2);
%yline(98.5,'--k','LineWidth',lw2);
yline(10.43,'-','LineWidth',lw1, 'Color',color4); hold on;
yline(11.20,'--','LineWidth',lw2, 'Color', color3); hold on;

plotSK_JND(nTrials,twoPokeReversal, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);

xlim([1,50])
ylim([10,16])
%ylim([90 120]);
xlabel('Trial Number')
ylabel('Actuator Command (mm)')
ax.FontSize = 15;

leg = legend('', '', '', 'Reference', 'JND', '', '', 'Reversal');
set(leg, 'edgeColor','w', 'Location','northeast');

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

%p = plot(nTrials, twoPokeTestMM, '-o', 'LineWidth',lw2, 'Color', color2, 'MarkerSize', 5, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2); hold on;

plotSK_JND(nTrials,onePokeTestMM, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
%yline(95,'-k','LineWidth',lw2);
%yline(103.1,'-k','LineWidth',lw2);

yline(10.43,'-','LineWidth',lw1, 'Color',color4); hold on;
yline(12.20,'--','LineWidth',lw2, 'Color', color3); hold on;

plotSK_JND(nTrials,onePokeReversal, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);

xlim([1,50])
ylim([10,16])
%ylim([90 120]);
xlabel('Trial Number')
ylabel('Actuator Command (mm)')
ax.FontSize = 15;

leg = legend('', '', '', 'Reference', 'JND', '', '', 'Reversal');
set(leg, 'edgeColor','w', 'Location','northeast');

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);
ax.FontSize = 15;

s1 = subplot(2,1,2);
plotSK_JND(nTrials,twoPokeTestMM, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
yline(10.43,'-','LineWidth',lw1, 'Color',color4); hold on;
yline(10.72,'--','LineWidth',lw2, 'Color', color3); hold on;
plotSK_JND(nTrials,twoPokeReversal, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
ylim([10,16])
xlim([1,50])
xlabel('Two Contacts, Trial Number')
ylabel('Actuator Command (mm)')
s1.FontSize = 15;

s2 = subplot(2,1,1);
plotSK_JND(nTrials,onePokeTestMM, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
yline(10.43,'-','LineWidth',lw1, 'Color',color4); hold on;
yline(12.31,'--','LineWidth',lw2, 'Color', color3); hold on;
plotSK_JND(nTrials,onePokeReversal, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
ylim([10,16])
xlim([1,50])
xlabel('Single Contact, Trial Number')
ylabel('Actuator Command (mm)')
s2.FontSize = 15;
leg = legend('', '', '', 'Reference', 'JND', '', '', 'Reversal');
set(leg, 'edgeColor','w', 'Location','northeast');