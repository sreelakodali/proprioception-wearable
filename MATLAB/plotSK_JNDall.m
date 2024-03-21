function [] = plotSK_JNDall(file)

    close all
    color="#0C1446";%reversal
color2 = "#29A0B1";%staircase
color3 = "#FF9636"; %JND
color4 = "#190204"; %reference
color5 = "#4B8378";
color6 = "#DF362D";
color7 = "#880ED4";

path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/';

sz = 50;
j = 0;

onePoke = readmatrix(strcat(path,file, '/processed_', file,'.csv'),'NumHeaderLines',1);

%onePoke(idx_remove1,:) = [];
commandMM_1p = interp1([47, 139],[0, 20],onePoke(:,3));
measuredMM_1p = interp1([986, 100],[0, 20],onePoke(:,4));
force_1p = onePoke(:,5);
time = onePoke(:,1);
nTrials = onePoke(:,9);


%-------------
figure;
set(gcf,'color','white')
ax = gca(gcf);

plot(time,commandMM_1p, 'Color', color2); hold on;
plot(time,measuredMM_1p, 'Color', color5); hold on;
ax.FontSize = 15;
xlabel('One Contact, Actuator Command (mm)')
ylabel('Actuator Position')

yyaxis right

plot(time,force_1p, 'Color', color7); hold on;
ylabel("Force (N)", 'Color', color7)
ax.YAxis(2).Color = color7;

%----------------

figure;
set(gcf,'color','white')
ax = gca(gcf); 

b = boxchart(commandMM_1p,measuredMM_1p, 'BoxFaceColor',color2, 'MarkerColor',color2, 'MarkerStyle','o');
b.JitterOutliers = 'on';
b.BoxWidth = 0.2;
b.LineWidth = 1.5;
%b = boxchart([commandMM_1p; commandMM_1p],[measuredMM_1p; force_1p], 'GroupByColor', [ones(size(measuredMM_1p)); zeros(size(force_1p))]);
%b.JitterOutliers = 'on';
% b(1).BoxWidth = 0.2;
% b(1).LineWidth = 1.5;
% b(2).BoxWidth = 0.2;
% b(2).LineWidth = 1.5;
xlim([10,16])
ylim([7,16])
% ylim([5,20])
%xlim([90,120])
xticks(round(unique(commandMM_1p),1))
xlabel('One Contact, Actuator Command (mm)')
ylabel('Actuator Position')
ax.FontSize = 15;
ax.XTickLabelRotation = 45;


yyaxis right
% colormap("cool");
% scatter(commandMM_1p+j,force_1p,sz,commandMM_1p, 's', 'filled')
b = boxchart(commandMM_1p,force_1p, 'BoxFaceColor',color7, 'MarkerColor',color7, 'MarkerStyle','o');
b.JitterOutliers = 'on';
b.BoxWidth = 0.2;
b.LineWidth = 1.5;
ylabel("Force (N)", 'Color', color7)
ax.YAxis(2).Color = color7;
ylim([0,10])


figure;
set(gcf,'color','white')
s1 = gca(gcf); 

yyaxis left
scatter(commandMM_1p,measuredMM_1p,sz,commandMM_1p, 'o', 'filled')
colormap(s1, "winter");

% ylim([5,20])
xlim([10,16])
ylim([7,16])
%xlim([90,120])
xticks(round(unique(commandMM_1p),1))
xlabel('One Contact, Actuator Command (mm)')
ylabel('Actuator Position')
s1.FontSize = 15;
s1.XTickLabelRotation = 45;


yyaxis right
colormap("cool");
scatter(commandMM_1p+j,force_1p,sz,commandMM_1p, 'o', 'filled')
ylabel("Force (N)", 'Color', color7)
s1.YAxis(2).Color = color7;
ylim([0,10])
colormap(s1,"winter");

end