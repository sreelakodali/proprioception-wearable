color="#0C1446";%reversal
color2 = "#29A0B1";%staircase
color3 = "#FF9636"; %JND
color4 = "#190204"; %reference
color5 = "#4B8378";
color6 = "#DF362D";
color7 = "#880ED4";


close all;
figure;
set(gcf,'color','white')
s1 = gca(gcf); 
grad = [diff(measuredPos);0];
idx = find(abs(grad) <=0.024);

idx2 = 1025:25:2000;

idx3 = islocalmax(grad, 'MinSeparation',25);
idx3 = find(idx3);

% idx4 = [];
% for i = 1:(length(idx3) - 1)
%     idx4 = [idx4; floor((idx3(i) + idx3(i+1))/2) ];
% end
scatter(cmd, (measuredPos), 5, "cyan", 'filled'); hold on;
plot(cmd, grad); hold on;
scatter(cmd(idx), measuredPos(idx), 5, "red", 'filled'); hold on;
%scatter(cmd(idx3), grad(idx3), 10, "black", 'filled');
scatter(cmd(idx4), measuredPos(idx4), 10, "black", 'filled');

consolidatedCMD = cmd(idx4);
consolidatedMeasured = measuredPos(idx4);

figure;
set(gcf,'color','white')
s2 = gca(gcf); 
scatter(consolidatedCMD, consolidatedMeasured, 10, "cyan", 'filled'); hold on;

trueCommands = cmd(idx4)