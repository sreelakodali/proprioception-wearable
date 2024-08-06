close all
data = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/minMaxForce_MeanSTDperSubject_16.csv','NumHeaderLines',0);
disp(mean(data,1));
data = [data; [0, 0, 0, 0, 0]; mean(data,1)];


plotData = data(:,[2,4]);
plotData = abs(plotData);

color2 = "#75E6DA";%"#B00000";
color = "#189AB4";%"#189AB4"; %"#0000FF";%1/255*[231,188,188];
color3 = "#05445E";
lw = 1.5;
bw = 1;

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

b = bar(plotData, 'grouped', 'EdgeColor','none'); hold on;
set(b(1), 'FaceColor',color2, 'BarWidth', bw);
set(b(2), 'FaceColor',color);
xlabel('Subject Number')
ylabel('Force (N)')
ax.FontSize = 18;

[ngroups,nbars] = size(plotData);
% Get the x coordinate of the bars
z = nan(nbars, ngroups);
for i = 1:nbars
    z(i,:) = b(i).XEndPoints;
end

er = errorbar(z', plotData, data(:,[3,5]), 'color', color3, 'linestyle', 'none', 'linewidth', lw); hold on;
%er(1)(13).Color = 'w';
x = xline(15, ':', 'lineWidth', lw, 'Color',"#000000"); hold on;
xticks(1:1:16);
xticklabels({'1', '2','3','4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '', 'Group'})
xtickangle(0)
set(ax, 'TickLength', [0,0]);
leg = legend('Minimum Force','Maximum Force');
set(leg, 'edgeColor','w', 'Location','northeast');

%er(1).Color = color2;
% er.Color = color2;
% er.LineWidth = lw;
% er.LineStyle = 'none'; 

% er = errorbar(abs(data(:,2)),data(:,3)); hold on; 
% er.Color = color2;
% er.LineWidth = lw;
% er.LineStyle = 'none';  

 