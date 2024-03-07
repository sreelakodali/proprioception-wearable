% Looking at JND study data
% Written by Sreela Kodali kodali@stanford.edu

close all
clear
color="#0C1446";%reversal
color2 = "#29A0B1";%staircase
color3 = "#FF2101"; %JND
sz = 10;

twoPoke = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/bloop4.csv','NumHeaderLines',1);

twoPoke(1,:) = [];
commands = twoPoke(:,1);
commandPosition = twoPoke(:,2);
measuredPosition = twoPoke(:,4);
measuredErr = twoPoke(:,8);
force = twoPoke(:,9);
forceErr = twoPoke(:,12);

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);
plot(commands,commandPosition,'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color); hold on;
plot(commands,measuredPosition,'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2); hold on;
xlim([90,120])
ylim([5,20])
xlabel('Actuator Command (pwm)')
ylabel('Actuator Position (mm)')
ax.FontSize = 15;

yyaxis right
ylabel("Force (N)", 'Color', 'black')
set(ax, 'YColor', 'r');
ylim([0,10])
plot(commands,force,'square', 'MarkerSize', sz, 'MarkerEdgeColor', color3, 'MarkerFaceColor', color3); hold on;

leg = legend('Commanded Position', 'Measured Position', 'Force');
set(leg, 'edgeColor','w', 'Location','northeast');

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);
plot(commandPosition,force,'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color); hold on;
plot(measuredPosition,force,'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2); hold on;
% xlim([90,120])
% ylim([5,20])
xlabel('Actuator Position (mm)')
ylabel('Force (N)')
ax.FontSize = 15;

leg = legend('Commanded Position', 'Measured Position');
set(leg, 'edgeColor','w', 'Location','northeast');


figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);
plot(commandPosition,measuredPosition,'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2); hold on;
e = errorbar(commandPosition,measuredPosition,measuredErr,"o", 'Color',color2, 'LineWidth',2); hold on;
% xlim([90,120])
% ylim([5,20])
xlabel('Actuator Command (mm)')
ylabel('Measured Actuator Position (mm)')
ax.FontSize = 15;

yyaxis right
ylabel("Force (N)", 'Color', 'black')
set(ax, 'YColor', 'r');
%ylim([0,10])
plot(commandPosition,force,'s', 'MarkerSize', sz, 'MarkerEdgeColor', color3, 'MarkerFaceColor', color3); hold on;
e = errorbar(commandPosition,force,forceErr,"o", 'Color',color3, 'LineWidth',2); hold on;
leg = legend('Measured Position', '', 'Force');
set(leg, 'edgeColor','w', 'Location','northeast');