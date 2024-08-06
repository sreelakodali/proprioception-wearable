close all
% nHnV = ABSError(1:14);
% nHV = ABSError(15:28);
% HnV = ABSError(29:42);
% HV = ABSError(43:56);


nHnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/avgnHnV_pythonGenerated_16.csv','NumHeaderLines',0);
nHV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/avgnHV_pythonGenerated_16.csv','NumHeaderLines',0);
HnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/avgHnV_pythonGenerated_16.csv','NumHeaderLines',0);
HV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/avgHV_pythonGenerated_16.csv','NumHeaderLines',0);

errorNotAbs = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/error_notABS.csv','NumHeaderLines',0);



nHnV = nHnV(:,4);
nHV = nHV(:,4);
HnV = HnV(:,4);
HV = HV(:,4);

HV([2, 8], :) = [];
nHnV([2, 8], :) = [];
nHV([2, 8], :) = [];
HnV([2, 8], :) = [];

mean_nHnV = mean(nHnV);
mean_nHV = mean(nHV);
mean_HnV = mean(HnV);
mean_HV = mean(HV);

x = [0, 1];

y = [mean_nHnV, mean_HnV];
% color = "#361AE5";
% color2 = "#91B5BB";
% color = "#880ED4";%"#0093AC";%"#B00000";
% color2 = "#BD97CB";
% color = "#B02C3A";%"#0093AC";%"#B00000";
% color2 = "#C09C9F";%
color = "#B02C3A";%"#0093AC";%"#B00000";
color2 = "#C09C9F";%"#91B5BB";%"#C49F98";%"#189AB4"; %"#0000FF";%1/255*[231,188,188];
color3 = "#880ED4";%"#361AE5";%"#0093AC";%"#B00000";
color4 = "#BD97CB";%"#91B5BB";%"#91B5BB";%"#C49F98";%"#189AB4"; %"#0000FF";%1/255*[231,188,188];
avg = mean(errorNotAbs);
disp(avg);
nV = [avg(3), avg(1)]*-1;
V = [avg(4), avg(2)];

sz = 20;
fz= 18;
fz2 = fz;
lw = 3;
j = 0.05;

figure

p = plot(x, y, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color);

fig = gcf;
set(gcf,'color','white')

ax = gca(fig);
ax.FontSize = fz;
p.Color = color;
%p.LineWidth = 2.2;
xlim([-0.5, 1.5])
ylim([-1, 25])
xticks([-0.5, 0, 1, 1.5])
xticklabels({'', 'No Haptics', 'Haptics', ''})


hold on;
y2 = [mean_nHV, mean_HV];
p2 = plot(x-j, y2, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2);
p2.Color = color2;
p2.LineWidth = 2.2;

hold on;
p3 = plot(x, nV, 's', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color);
p3.Color = color3;

hold on;
p4 = plot(x+j, V, 's', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2);
p4.Color = color4;

%title("No Haptics vs Haptics")
ylabel("Mean Error (deg)")
grid off
ax.XGrid = 'off';
ax.YGrid = 'off';

stdErr = std([nHnV, HnV])/sqrt(length(nHnV));
stdErr2 = std([nHV, HV])/sqrt(length(nHV));
hold on;
e = errorbar(x, y, stdErr);
e.Color = color;
e.LineWidth = lw;
e.LineStyle = "--";


hold on;
e2 = errorbar(x, y2, stdErr2);
e2.Color = color2;
e2.LineWidth = lw;
e2.LineStyle = "--";

hold on;
totalStdErr = std(errorNotAbs)/sqrt(14);
stdErr3 = [totalStdErr(3),totalStdErr(1)];
stdErr4 = [totalStdErr(4),totalStdErr(2)];
e3 = errorbar(x, nV, stdErr3);
e3.Color = color;
e3.LineWidth = lw;
e3.LineStyle = "--";


hold on;
e4 = errorbar(x+j, V, stdErr4);
e4.Color = color2;
e4.LineWidth = lw;
e4.LineStyle = "--";

b = plot(-5, -5, 'o', 'MarkerSize', sz, 'LineWidth', 2, 'MarkerEdgeColor', 'k');
a = plot(-5, -5, 's', 'MarkerSize', sz, 'LineWidth', 2, 'MarkerEdgeColor', 'k');



a3 = annotation('textbox', [0.15, 0.65, 0.1, 0.1], 'String', "No Visual", 'FontSize', fz2, 'Color', color, 'EdgeColor', 'white');
a4 = annotation('textbox', [0.15, 0.15, 0.1, 0.1], 'String', "Visual", 'FontSize', fz2, 'Color', color2, 'EdgeColor', 'white');
hold on;

leg = legend('', '', '', '', '', '', '', '', 'Angle Error Magnitude', 'Angle Error');
set(leg, 'edgeColor','w', 'Location','northeast');

%breakyaxis([3 15]);


hold off

% figure
% 
% p = plot(x, y, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color);
% 
% fig = gcf;
% set(gcf,'color','white')
% 
% ax = gca(fig);
% ax.FontSize = fz;
% p.Color = color;
% %p.LineWidth = 2.2;
% xlim([-0.5, 1.5])
% ylim([0, 26])
% xticks([-0.5, 0, 1, 1.5])
% xticklabels({'', 'No Haptics', 'Haptics', ''})
% 
% 
% hold on
% y2 = [mean_nHV, mean_HV];
% p2 = plot(x, y2, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2);
% p2.Color = color2;
% %p2.LineWidth = 2.2;
% 
% %title("No Haptics vs Haptics")
% ylabel("Mean Angle Error (deg)")
% grid off
% ax.XGrid = 'off';
% 
% stdErr = std([nHnV, HnV])/sqrt(length(nHnV));
% stdErr2 = std([nHV, HV])/sqrt(length(nHV));
% hold on
% e = errorbar(x, y, stdErr);
% e.Color = color;
% e.LineWidth = lw;
% e.LineStyle = "--";
% 
% 
% hold on
% e2 = errorbar(x, y2, stdErr2);
% e2.Color = color2;
% e2.LineWidth = lw;
% e2.LineStyle = "--";
% 
% 
% a3 = annotation('textbox', [0.7, 0.5, 0.1, 0.1], 'String', "No Visual", 'FontSize', fz2, 'Color', color, 'EdgeColor', 'white');
% a4 = annotation('textbox', [0.75, 0.1, 0.1, 0.1], 'String', "Visual", 'FontSize', fz2, 'Color', color2, 'EdgeColor', 'white');
% 
% breakyaxis([3 12]);
% hold off
% 
% % figure
% % x = 0:.1:1;
% % y = (mean_HV-mean_nHnV)*x + mean_nHnV;
% % z = zeros(size(x));
% % col = x;  % This is the color, vary with x in this case.
% % surface([x;x],[y;y],[z;z],[col;col],...
% %         'facecol','no',...
% %         'edgecol','interp',...
% %         'linew',2); hold on;
% % c = flip(hot(100));
% % colorFactor = ceil(10*F_avgHnV);
% % cmap = zeros(10,3);
% % for i = 1:10
% %     cmap(i,:) = c(colorFactor(i)+50,:);
% % end
% % colormap(cmap);
% 
% 
