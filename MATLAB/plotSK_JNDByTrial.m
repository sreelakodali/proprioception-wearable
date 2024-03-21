function [] = plotSK_JNDByTrial(file)

%onePoke_2024-03-18_22-21

 close all
 color="#0C1446";%reversal
color2 = "#29A0B1";%staircase
color3 = "#FF9636"; %JND
color4 = "#190204"; %reference
color5 = "#4B8378";
color6 = "#DF362D";
color7 = "#880ED4";
sz = 10;

path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/';
onePoke = readmatrix(strcat(path, 'force_AND_Position_OfStairCase_', file, '.csv'),'NumHeaderLines',1);
nTrials = onePoke(:,1);
onePokeTest = onePoke(:,2);
onePokeTestMM = onePoke(:,3);
onePokeForce = onePoke(:,4);
stdev_onePokeForce = onePoke(:,5);
onePokeMeasuredPos = onePoke(:,6);
stdev_onePokeMeasuredPos = onePoke(:,7);
n_onePoke = onePoke(:,12);
stderr_onePokeMeasuredPos = stdev_onePokeMeasuredPos ./ sqrt(n_onePoke);
stderr_onePokeForce = stdev_onePokeForce ./ sqrt(n_onePoke);


j = 1;
sz = 5;
lw2 = 2;
lw1 = 1;

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

noStdev = zeros(size(onePokeTest));
plotSK_JND(nTrials,onePokeTestMM, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,onePokeMeasuredPos, stderr_onePokeMeasuredPos, color5, 0, sz, j, lw1, lw2, 0, 0, []);
ylim([5,20])
xlim([1,50])
xlabel(strcat(file, ' Trial Number'))
ylabel('Actuator Command (mm)')
ax.FontSize = 15;

yyaxis right
ylabel("Force (N)", 'Color', color3)
ax.YAxis(2).Color = color3;
ylim([0,10])

plot(nTrials,onePokeForce,'-', 'Color', color3, 'LineWidth',lw2); hold on;
plotSK_JND(nTrials,onePokeForce, 1*stderr_onePokeForce, color3, 0, sz, j, lw1, lw2, 0, 0, []);


% ---- normalized
figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

onePokeTestMM_Normalized = onePokeTestMM - onePokeTestMM(1,1);
onePokeMeasuredPos_Normalized = onePokeMeasuredPos - onePokeMeasuredPos(1,1);

plotSK_JND(nTrials,onePokeTestMM_Normalized, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,onePokeMeasuredPos_Normalized, stderr_onePokeMeasuredPos, color5, 0, sz, j, lw2, lw2, 0, 0, []);

ylim([-6,0])
xlim([1,50])
xlabel('One Contact, Trial Number')
ylabel('Actuator Position Difference (mm)')
ax.FontSize = 15;

yyaxis right
ylabel("Force (N)", 'Color', color3)
ax.YAxis(2).Color = color3;
ylim([4,10])

plot(nTrials,onePokeForce,'-', 'Color', color3, 'LineWidth',lw2); hold on;
%plot(nTrials,onePokeForce,'-o', 'MarkerSize', 6, 'Color', color3, 'MarkerEdgeColor', color3, 'MarkerFaceColor', color3, 'LineWidth',lw2); hold on;
plotSK_JND(nTrials,onePokeForce, 1*stderr_onePokeForce, color3, 0, sz, j, lw1, lw2, 0, 0, []);
end