function [allData] = plotSK_JNDall2(data)
    color="#0C1446";%reversal
color2 = "#29A0B1";%staircase
color3 = "#FF9636"; %JND
color4 = "#190204"; %reference
color5 = "#4B8378";
color6 = "#DF362D";
color7 = "#880ED4";
sz = 50;
j = 0;


allData = [];
for i = 1:size(data,1)
    c = cell2mat(data(i,3)) * ones(size(cell2mat(data(i,1)),1),1);
    f = cell2mat(data(i,1));
    m = cell2mat(data(i,2));
    newData = [f, m, c];
    allData = [allData; newData];

end

commandMM_1p = allData(:,3);
measuredMM_1p = allData(:,2);
force_1p = allData(:,1);

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
ylim([0,16])
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
ylim([3,8])


figure;
set(gcf,'color','white')
s1 = gca(gcf); 

yyaxis left
scatter(commandMM_1p,measuredMM_1p,sz,commandMM_1p, 'o', 'filled')
colormap(s1, "winter");

% ylim([5,20])
xlim([10,16])
ylim([0,16])
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
ylim([3,8])
colormap(s1,"winter");

end