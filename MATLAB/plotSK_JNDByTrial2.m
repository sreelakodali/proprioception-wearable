function [] = plotSK_JNDByTrial2(data)

 %close all
 color="#0C1446";%reversal
color2 = "#29A0B1";%staircase
color3 = "#FF9636"; %JND
color4 = "#190204"; %reference
color5 = "#4B8378";
color6 = "#DF362D";
color7 = "#880ED4";
sz = 10;


nTrials = 1:50;
onePokeTestMM = cell2mat(data(3,:));

onePokeForce = [];
stdev_onePokeForce = [];
n_onePoke = [];
onePokeMeasuredPos = [];
stdev_onePokeMeasuredPos = [];

for i = data(1,:)
    onePokeForce(end+1) = mean(cell2mat(i));
    stdev_onePokeForce(end+1) = std(cell2mat(i));
    n_onePoke(end+1) = length(cell2mat(i));
end

for i = data(2,:)
    onePokeMeasuredPos(end+1) = mean(cell2mat(i));
    stdev_onePokeMeasuredPos(end+1) = std(cell2mat(i));
end


stderr_onePokeMeasuredPos = stdev_onePokeMeasuredPos ./ sqrt(n_onePoke);
stderr_onePokeForce = stdev_onePokeForce ./ sqrt(n_onePoke);


j = 1;
sz = 5;
lw2 = 2;
lw1 = 1;

figure;
set(gcf,'color','white')
ax = gca(gcf);

noStdev = zeros(size(onePokeTestMM));
plotSK_JND(nTrials,onePokeTestMM, noStdev, color2, 0, sz, j, lw1, lw2, 0, 0, []);
plotSK_JND(nTrials,onePokeMeasuredPos, stderr_onePokeMeasuredPos, color5, 0, sz, j, lw1, lw2, 0, 0, []);
ylim([5,20])
xlim([1,50])
xlabel('Trial Number')
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