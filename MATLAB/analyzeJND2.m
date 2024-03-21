% Looking at JND study data 2
% Written by Sreela Kodali kodali@stanford.edu

close all
clear
color="#0C1446";%reversal
color2 = "#29A0B1";%staircase
color3 = "#FF9636"; %JND
color4 = "#190204"; %reference
color5 = "#4B8378";
color6 = "#DF362D";

sz = 10;

twoPoke = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/force_AND_Position_OfStairCase_twoPoke_2024-01-30_20-21.csv','NumHeaderLines',1);
onePoke = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/force_AND_Position_OfStairCase_onePoke_2024-01-30_20-47.csv','NumHeaderLines',1);

nTrials = twoPoke(:,1);
twoPokeTest = twoPoke(:,2);
twoPokeTestMM = twoPoke(:,3);
twoPokeForce = twoPoke(:,4);
stdev_twoPokeForce = twoPoke(:,5);
twoPokeMeasuredPos = twoPoke(:,6);
stdev_twoPokeMeasuredPos = twoPoke(:,7);
n_twoPoke = twoPoke(:,12);
stderr_twoPokeMeasuredPos = stdev_twoPokeMeasuredPos ./ sqrt(n_twoPoke);
stderr_twoPokeForce = stdev_twoPokeForce ./ sqrt(n_twoPoke);


onePokeTest = onePoke(:,2);
onePokeTestMM = onePoke(:,3);
onePokeForce = onePoke(:,4);
stdev_onePokeForce = onePoke(:,5);
onePokeMeasuredPos = onePoke(:,6);
stdev_onePokeMeasuredPos = onePoke(:,7);
n_onePoke = onePoke(:,12);
stderr_onePokeMeasuredPos = stdev_onePokeMeasuredPos ./ sqrt(n_onePoke);
stderr_onePokeForce = stdev_onePokeForce ./ sqrt(n_onePoke);


idx_twoPokeReversals = [9, 11, 14, 16, 19, 23, 27, 29, 32, 34, 37, 39, 42, 44, 47, 49];
idx_onePokeReversals = [9, 11, 13, 15, 17, 19, 22, 24, 26, 28, 30, 32, 37, 39, 41, 43];

idx_2P_MeasuredPosReversalsY = [9, 11, 14, 16, 19, 23, 27, 29, 32, 34, 37, 39, 42, 44, 47, 49];
idx_1P_MeasuredPosReversalsY = [9, 11, 13, 15, 17, 19, 22, 24, 26, 28, 30, 32, 37, 39, 41, 43];
%idx_1P_MeasuredPosReversalsY = [9, 13, 19, 22, 24, 26, 30, 37, 39, 41, 43];
idx_2P_MeasuredPosReversalsN = [];
idx_1P_MeasuredPosReversalsN = [];
%idx_1P_MeasuredPosReversalsN = [10, 14, 16, 27, 31];


idx_2P_ForceReversalsY = [9, 11, 14, 16, 19, 23, 27, 29, 32, 34, 37, 39, 42, 44, 47, 49];
idx_1P_ForceReversalsY = [9, 11, 13, 15, 17, 19, 22, 24, 26, 28, 30, 32, 37, 39, 41, 43];
idx_2P_ForceReversalsN = [];
idx_1P_ForceReversalsN = [10, 11, 14, 15, 23, 24, 29, 30, 31, 32];





twoPokeReversalMask = zeros(50,1);
onePokeReversalMask = zeros(50,1);
twoPokeReversalMask(idx_twoPokeReversals) = 1;
onePokeReversalMask(idx_onePokeReversals) = 1;
twoPokeReversalTestMM = twoPokeReversalMask .* twoPokeTestMM;
onePokeReversalTestMM = onePokeReversalMask .* onePokeTestMM;


twoPokeReversalMask = zeros(50,1);
onePokeReversalMask = zeros(50,1);
twoPokeReversalMask(idx_2P_MeasuredPosReversalsY) = 1;
onePokeReversalMask(idx_1P_MeasuredPosReversalsY) = 1;
twoPokeReversalMeasuredMMY = twoPokeReversalMask .* twoPokeMeasuredPos;
onePokeReversalMeasuredMMY = onePokeReversalMask .* onePokeMeasuredPos;

twoPokeReversalMask = zeros(50,1);
onePokeReversalMask = zeros(50,1);
twoPokeReversalMask(idx_2P_MeasuredPosReversalsN) = 1;
onePokeReversalMask(idx_1P_MeasuredPosReversalsN) = 1;
twoPokeReversalMeasuredMMN = twoPokeReversalMask .* twoPokeMeasuredPos;
onePokeReversalMeasuredMMN = onePokeReversalMask .* onePokeMeasuredPos;

twoPokeReversalMask = zeros(50,1);
onePokeReversalMask = zeros(50,1);
twoPokeReversalMask(idx_2P_ForceReversalsY) = 1;
onePokeReversalMask(idx_1P_ForceReversalsY) = 1;
twoPokeReversalForceY = twoPokeReversalMask .* twoPokeForce;
onePokeReversalForceY = onePokeReversalMask .* onePokeForce;
twoPokeReversalForceY(twoPokeReversalForceY == 0) = -1;
onePokeReversalForceY(onePokeReversalForceY == 0) = -1;

twoPokeReversalMask = zeros(50,1);
onePokeReversalMask = zeros(50,1);
twoPokeReversalMask(idx_2P_ForceReversalsN) = 1;
onePokeReversalMask(idx_1P_ForceReversalsN) = 1;
twoPokeReversalForceN = twoPokeReversalMask .* twoPokeForce;
onePokeReversalForceN = onePokeReversalMask .* onePokeForce;
twoPokeReversalForceN(twoPokeReversalForceN == 0) = -1;
onePokeReversalForceN(onePokeReversalForceN == 0) = -1;


j = 1;
sz = 5;
lw2 = 2;
lw1 = 1;

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

noStdev = zeros(size(twoPokeTest));


s1 = subplot(2,1,2);
plotSK_JND(nTrials,twoPokeTestMM, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,twoPokeMeasuredPos, stderr_twoPokeMeasuredPos, color5, 0, sz, j, lw1, lw2, 0, 0, []);
% yline(10.43,'-','LineWidth',lw1, 'Color',color4); hold on;
% yline(10.72,'--','LineWidth',lw2, 'Color', color3); hold on;
plotSK_JND(nTrials,twoPokeReversalTestMM, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
plotSK_JND(nTrials,twoPokeReversalMeasuredMMY, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
%plotSK_JND(nTrials,twoPokeReversalMeasuredMMN, noStdev, color6, 0, sz, j, lw1, lw2, 1, 0, []);

ylim([5,20])
xlim([1,50])
xlabel('Two Contacts, Trial Number')
ylabel('Actuator Command (mm)')
s1.FontSize = 15;

yyaxis right
ylabel("Force (N)", 'Color', color3)
s1.YAxis(2).Color = color3;
ylim([0,10])
plot(nTrials,twoPokeForce,'-', 'Color', color3, 'LineWidth',lw2); hold on;
%plot(nTrials,twoPokeForce,'-o', 'MarkerSize', 6, 'Color', color3, 'MarkerEdgeColor', color3, 'MarkerFaceColor', color3, 'LineWidth',lw2); hold on;
plotSK_JND(nTrials,twoPokeForce, stderr_twoPokeForce, color3, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,twoPokeReversalForceY, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
%plotSK_JND(nTrials,twoPokeReversalForceN, noStdev, color6, 0, sz, j, lw1, lw2, 1, 0, []);

leg = legend('', 'Commanded Position', '', '', 'Measured Position','', '', '', 'Reversal');
set(leg, 'edgeColor','w', 'Location','northeast');

s2 = subplot(2,1,1);
plotSK_JND(nTrials,onePokeTestMM, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,onePokeMeasuredPos, stderr_onePokeMeasuredPos, color5, 0, sz, j, lw1, lw2, 0, 0, []);
% yline(10.43,'-','LineWidth',lw1, 'Color',color4); hold on;
% yline(12.31,'--','LineWidth',lw2, 'Color', color3); hold on;
plotSK_JND(nTrials,onePokeReversalTestMM, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
plotSK_JND(nTrials,onePokeReversalMeasuredMMY, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
plotSK_JND(nTrials,onePokeReversalMeasuredMMN, noStdev, color6, 0, sz, j, lw1, lw2, 1, 0, []);

ylim([5,20])
xlim([1,50])
xlabel('Single Contact, Trial Number')
ylabel('Actuator Command (mm)')
s2.FontSize = 15;

yyaxis right
ylabel("Force (N)", 'Color', color3)
s2.YAxis(2).Color = color3;
ylim([0,10])

plot(nTrials,onePokeForce,'-', 'Color', color3, 'LineWidth',lw2); hold on;
%plot(nTrials,onePokeForce,'-o', 'MarkerSize', 6, 'Color', color3, 'MarkerEdgeColor', color3, 'MarkerFaceColor', color3, 'LineWidth',lw2); hold on;
plotSK_JND(nTrials,onePokeForce, 1*stderr_onePokeForce, color3, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,onePokeReversalForceY, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
plotSK_JND(nTrials,onePokeReversalForceN, noStdev, color6, 0, sz, j, lw1, lw2, 1, 0, []);


leg = legend('', '', '', '', '','', '', '', '', '', '', '', '', '', 'Errors', 'Force');
set(leg, 'edgeColor','w', 'Location','northeast');




% -----------------------------------------------
% let's try to normalize the actuator positions

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

onePokeTestMM_Normalized = onePokeTestMM - onePokeTestMM(1,1);
onePokeMeasuredPos_Normalized = onePokeMeasuredPos - onePokeMeasuredPos(1,1);
onePokeReversalTestMM_Normalized = onePokeReversalTestMM - onePokeTestMM(1,1);
onePokeReversalMeasuredMMY_Normalized = onePokeReversalMeasuredMMY - onePokeMeasuredPos(1,1);

s3 = subplot(2,1,1);
plotSK_JND(nTrials,onePokeTestMM_Normalized, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,onePokeMeasuredPos_Normalized, stderr_onePokeMeasuredPos, color5, 0, sz, j, lw2, lw2, 0, 0, []);
plotSK_JND(nTrials,onePokeReversalTestMM_Normalized, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
plotSK_JND(nTrials,onePokeReversalMeasuredMMY_Normalized, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);

ylim([-6,0])
xlim([1,50])
xlabel('One Contact, Trial Number')
ylabel('Actuator Position Difference (mm)')
s3.FontSize = 15;

yyaxis right
ylabel("Force (N)", 'Color', color3)
s3.YAxis(2).Color = color3;
ylim([4,10])

plot(nTrials,onePokeForce,'-', 'Color', color3, 'LineWidth',lw2); hold on;
%plot(nTrials,onePokeForce,'-o', 'MarkerSize', 6, 'Color', color3, 'MarkerEdgeColor', color3, 'MarkerFaceColor', color3, 'LineWidth',lw2); hold on;
plotSK_JND(nTrials,onePokeForce, 1*stderr_onePokeForce, color3, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,onePokeReversalForceY, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
%plotSK_JND(nTrials,onePokeReversalForceN, noStdev, color6, 0, sz, j, lw1, lw2, 1, 0, []);



% -------- Two Pokes


twoPokeTestMM_Normalized = twoPokeTestMM - twoPokeTestMM(1,1);
twoPokeMeasuredPos_Normalized = twoPokeMeasuredPos - twoPokeMeasuredPos(1,1);
twoPokeReversalTestMM_Normalized = twoPokeReversalTestMM - twoPokeTestMM(1,1);
twoPokeReversalMeasuredMMY_Normalized = twoPokeReversalMeasuredMMY - twoPokeMeasuredPos(1,1);


s4 = subplot(2,1,2);
plotSK_JND(nTrials,twoPokeTestMM_Normalized, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,twoPokeMeasuredPos_Normalized, stderr_twoPokeMeasuredPos, color5, 0, sz, j, lw2, lw2, 0, 0, []);
plotSK_JND(nTrials,twoPokeReversalTestMM_Normalized, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
plotSK_JND(nTrials,twoPokeReversalMeasuredMMY_Normalized, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);

ylim([-6,0])
xlim([1,50])
xlabel('Two Contacts, Trial Number')
ylabel('Actuator Position Difference (mm)')
s4.FontSize = 15;



yyaxis right
ylabel("Force (N)", 'Color', color3)
s4.YAxis(2).Color = color3;
ylim([4,10])
plot(nTrials,twoPokeForce,'-', 'Color', color3, 'LineWidth',lw2); hold on;
%plot(nTrials,twoPokeForce,'-o', 'MarkerSize', 6, 'Color', color3, 'MarkerEdgeColor', color3, 'MarkerFaceColor', color3, 'LineWidth',lw2); hold on;
plotSK_JND(nTrials,twoPokeForce, stderr_twoPokeForce, color3, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,twoPokeReversalForceY, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
%plotSK_JND(nTrials,twoPokeReversalForceN, noStdev, color6, 0, sz, j, lw1, lw2, 1, 0, []);


% ---------------

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

onePokeTestMM_Normalized = onePokeTestMM - onePokeTestMM(1,1);
onePokeMeasuredPos_Normalized = onePokeMeasuredPos - onePokeMeasuredPos(1,1);
onePokeReversalTestMM_Normalized = onePokeReversalTestMM - onePokeTestMM(1,1);
onePokeReversalMeasuredMMY_Normalized = onePokeReversalMeasuredMMY - onePokeMeasuredPos(1,1);

s3 = subplot(2,1,1);
plotSK_JND(nTrials,onePokeTestMM_Normalized, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,onePokeMeasuredPos_Normalized, stderr_onePokeMeasuredPos, color5, 0, sz, j, lw2, lw2, 0, 0, []);
plotSK_JND(nTrials,onePokeReversalTestMM_Normalized, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
plotSK_JND(nTrials,onePokeReversalMeasuredMMY_Normalized, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);

ylim([-6,0])
xlim([1,50])
xlabel('One Contact, Trial Number')
ylabel('Actuator Position Difference (mm)')
s3.FontSize = 15;

% yyaxis right
% ylabel("Force (N)", 'Color', color3)
% s3.YAxis(2).Color = color3;
% ylim([4,10])
% 
% plot(nTrials,onePokeForce,'-', 'Color', color3, 'LineWidth',lw2); hold on;
% %plot(nTrials,onePokeForce,'-o', 'MarkerSize', 6, 'Color', color3, 'MarkerEdgeColor', color3, 'MarkerFaceColor', color3, 'LineWidth',lw2); hold on;
% plotSK_JND(nTrials,onePokeForce, 1*stderr_onePokeForce, color3, 0, sz, j, lw1, lw2, 0, 0, []);
% plotSK_JND(nTrials,onePokeReversalForceY, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
% %plotSK_JND(nTrials,onePokeReversalForceN, noStdev, color6, 0, sz, j, lw1, lw2, 1, 0, []);



% -------- Two Pokes


twoPokeTestMM_Normalized = twoPokeTestMM - twoPokeTestMM(1,1);
twoPokeMeasuredPos_Normalized = twoPokeMeasuredPos - twoPokeMeasuredPos(1,1);
twoPokeReversalTestMM_Normalized = twoPokeReversalTestMM - twoPokeTestMM(1,1);
twoPokeReversalMeasuredMMY_Normalized = twoPokeReversalMeasuredMMY - twoPokeMeasuredPos(1,1);


s4 = subplot(2,1,2);
plotSK_JND(nTrials,twoPokeTestMM_Normalized, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,twoPokeMeasuredPos_Normalized, stderr_twoPokeMeasuredPos, color5, 0, sz, j, lw2, lw2, 0, 0, []);
plotSK_JND(nTrials,twoPokeReversalTestMM_Normalized, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
plotSK_JND(nTrials,twoPokeReversalMeasuredMMY_Normalized, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);

ylim([-6,0])
xlim([1,50])
xlabel('Two Contacts, Trial Number')
ylabel('Actuator Position Difference (mm)')
s4.FontSize = 15;

% yyaxis right
% ylabel("Force (N)", 'Color', color3)
% s4.YAxis(2).Color = color3;
% ylim([4,10])
% plot(nTrials,twoPokeForce,'-', 'Color', color3, 'LineWidth',lw2); hold on;
% %plot(nTrials,twoPokeForce,'-o', 'MarkerSize', 6, 'Color', color3, 'MarkerEdgeColor', color3, 'MarkerFaceColor', color3, 'LineWidth',lw2); hold on;
% plotSK_JND(nTrials,twoPokeForce, stderr_twoPokeForce, color3, 0, sz, j, lw1, lw2, 0, 0, []);
% plotSK_JND(nTrials,twoPokeReversalForceY, noStdev, color, 0, sz, j, lw1, lw2, 1, 0, []);
% %plotSK_JND(nTrials,twoPokeReversalForceN, noStdev, color6, 0, sz, j, lw1, lw2, 1, 0, []);

% --------------
figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

sortedTwoPoke = sortrows(twoPoke,2);

scatter(sortedTwoPoke(:,2), sortedTwoPoke(:,4), 'MarkerFaceColor', color2, 'MarkerEdgeColor',color2)


j = 1;
measuredBuf = [];
forceBuf = [];
uniqueCommands = unique(sortedTwoPoke(:,2));
new = zeros(size(uniqueCommands,1), 7);

for i = 1:size(sortedTwoPoke,1)
    if (sortedTwoPoke(i,2) ~= uniqueCommands(j))
        meanMeasured = sum(measuredBuf)/length(measuredBuf);
	    stdevMeasured = std(measuredBuf);
		nMeasured = length(measuredBuf);

		meanForce = sum(forceBuf)/length(forceBuf);
		stdevForce = std(forceBuf);
		nForce = length(forceBuf);

        new(j,:) = [uniqueCommands(j), meanMeasured, stdevMeasured, nMeasured, meanForce, stdevForce, nForce];
        disp(new(j,:))
        j = j + 1;
        measuredBuf = [];
		forceBuf = [];
    end
    measuredBuf(end+1) = sortedTwoPoke(i,6);
    forceBuf(end+1) = sortedTwoPoke(i,4);

end

meanMeasured = sum(measuredBuf)/length(measuredBuf);
stdevMeasured = std(measuredBuf);
nMeasured = length(measuredBuf);

meanForce = sum(forceBuf)/length(forceBuf);
stdevForce = std(forceBuf);
nForce = length(forceBuf);

new(j,:) = [uniqueCommands(j), meanMeasured, stdevMeasured, nMeasured, meanForce, stdevForce, nForce];
disp(new(j,:))

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);
scatter(new(:,2), new(:,5), 'MarkerFaceColor', color2, 'MarkerEdgeColor',color2)


