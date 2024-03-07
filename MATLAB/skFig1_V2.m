close all
% nHnV = ABSError(1:14);
% nHV = ABSError(15:28);
% HnV = ABSError(29:42);
% HV = ABSError(43:56);


nHnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/avgnHnV_pythonGenerated.csv','NumHeaderLines',0);
nHV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/avgnHV_pythonGenerated.csv','NumHeaderLines',0);
HnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/avgHnV_pythonGenerated.csv','NumHeaderLines',0);
HV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/processedDataCsvs/avgHV_pythonGenerated.csv','NumHeaderLines',0);

nHnV = nHnV(:,4);
nHV = nHV(:,4);
HnV = HnV(:,4);
HV = HV(:,4);

HV(8,:) = [];
nHnV(8,:) = [];
nHV(8,:) = [];
HnV(8,:) = [];

mean_nHnV = mean(nHnV);
mean_nHV = mean(nHV);
mean_HnV = mean(HnV);
mean_HV = mean(HV);

x = [0, 1];

y = [mean_nHnV, mean_HnV];
% color = "#361AE5";
% color2 = "#91B5BB";
color = "#FF2101";%"#0093AC";%"#B00000";
color2 = "#000000";%"#91B5BB";%"#C49F98";%"#189AB4"; %"#0000FF";%1/255*[231,188,188];
sz = 15;
fz= 18;
fz2 = fz;
lw = 2;

figure

%p = plot(x, y, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color); hold on;

fig = gcf;
set(gcf,'color','white')

ax = gca(fig);
ax.FontSize = fz;
set(ax, 'Visible', 'on')

%p.LineWidth = 2.2;
xlim([-0.5, 1.5])
ylim([0, 28])
%yticks([0:7:28])
xticks([-0.5, 0, 1, 1.5])
xticklabels({'', 'No Haptics', 'Haptics', ''})

y2 = [mean_nHV, mean_HV];
%p2 = plot(x, y2, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2);
%p2.Color = color2;
%p2.LineWidth = 2.2;

%title("No Haptics vs Haptics")
grid off
ax.XGrid = 'off';
ax.YGrid = 'off';

stdErr = std([nHnV, HnV])/sqrt(length(nHnV));
stdErr2 = std([nHV, HV])/sqrt(length(nHV));
hold on;
e = errorbar(x, y, stdErr);
e.Color = color2;
e.LineWidth = lw;

% e = errorbar(x(2), y(2), stdErr(2));
% e.Color = color;
% e.LineWidth = lw;
%e.LineStyle = "--";


hold on;
e2 = errorbar(x, y2, stdErr2);
e2.Color = color2;
e2.LineWidth = lw;
% e2 = errorbar(x(2), y2(2), stdErr2(2));
% e2.Color = color;
% e2.LineWidth = lw;
%e2.LineStyle = "--";



a1 = annotation('textbox', [0.7, 0.65, 0.1, 0.1], 'String', "No Visual", 'FontSize', fz2, 'Color', color2, 'EdgeColor', 'white');
a2 = annotation('textbox', [0.7, 0.15, 0.1, 0.1], 'String', "Visual", 'FontSize', fz2, 'Color', color2, 'EdgeColor', 'white');
hold on;

x = 0:.1:1;
y = (mean_HnV-mean_nHnV)*x + mean_nHnV;
z = zeros(size(x));
col = x;  % This is the color, vary with x in this case.
surface([x;x],[y;y],[z;z],[col;col],...
        'facecol','no',...
        'edgecol','interp',...
        'linew',2); hold on;
c = flip(hot(100));
colorFactor = ceil(10*F_avgHnV);
cmap = zeros(10,3);
for i = 1:10
    cmap(i,:) = c(colorFactor(i)+36,:);
end
colormap(cmap);
hold on;
%breakyaxis([3 15]);

p = plot(x, y, '--', 'Marker', 'none'); hold on;
p.Color = 'white';
p.LineWidth = lw;
%p = plot([0], [mean_nHnV], 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2); hold on;



y = (mean_HV-mean_nHV)*x + mean_nHV;
z = zeros(size(x));
col = x;  % This is the color, vary with x in this case.
surface([x;x],[y;y],[z;z],[col;col],...
        'facecol','no',...
        'edgecol','interp',...
        'linew',2); hold on;
c = flip(hot(100));
colorFactor = ceil(10*F_avgHnV);
cmap = zeros(10,3);
for i = 1:10
    cmap(i,:) = c(colorFactor(i)+36,:);
end
colormap(cmap);
hold on;

p = plot(x, y, '--', 'Marker', 'none'); hold on;
p.Color = 'white';
p.LineWidth = lw;
p2 = plot([0, 0], [mean_nHV, mean_nHnV], 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2); hold on;
%p2 = plot([0], [mean_nHV], 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2); hold on;
%p2 = plot([1], [mean_HV], 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color); hold on;
p = plot([1, 1], [mean_HnV, mean_HV], 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color); hold on;

breakyaxis([3 15]);
ylabel("Mean Angle Error (deg)")

set(ax, 'Visible', 'on');
hold off