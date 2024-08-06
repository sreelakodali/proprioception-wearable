close all

errorNotAbs = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/error_notABS.csv','NumHeaderLines',0);

color = "#880ED4";%"#361AE5";%"#0093AC";%"#B00000";
color2 = "#BD97CB";%"#91B5BB";%"#91B5BB";%"#C49F98";%"#189AB4"; %"#0000FF";%1/255*[231,188,188];

sz = 20;
fz= 18;
fz2 = fz;
lw = 3;

avg = mean(errorNotAbs);
disp(avg);
x = [0, 1];
nV = [avg(3), avg(1)];
V = [avg(4), avg(2)];


figure
p = plot(x, nV, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color);
fig = gcf;
set(gcf,'color','white')

ax = gca(fig);
ax.FontSize = fz;
p.Color = color;
%p.LineWidth = 2.2;
xlim([-0.5, 1.5])
% ylim([0, 26])
xticks([-0.5, 0, 1, 1.5])
xticklabels({'', 'No Haptics', 'Haptics', ''})


hold on;
p2 = plot(x, V, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2);
p2.Color = color2;
%p2.LineWidth = 2.2;

%title("No Haptics vs Haptics")
ylabel("Mean Angle Error (deg)")
grid off
ax.XGrid = 'off';
ax.YGrid = 'off';

totalStdErr = std(errorNotAbs)/sqrt(14);
%disp(totalStdErr)
stdErr = [totalStdErr(3),totalStdErr(1)];
%disp(stdErr)
stdErr2 = [totalStdErr(4),totalStdErr(2)];
hold on;
e = errorbar(x, nV, stdErr);
e.Color = color;
e.LineWidth = lw;
e.LineStyle = "--";


hold on;
e2 = errorbar(x, V, stdErr2);
e2.Color = color2;
e2.LineWidth = lw;
e2.LineStyle = "--";

a1 = annotation('textbox', [0.75, 0.75, 0.1, 0.1], 'String', "Visual", 'FontSize', fz2, 'Color', color2, 'EdgeColor', 'white');
a2 = annotation('textbox', [0.75, 0.45, 0.1, 0.1], 'String', "No Visual", 'FontSize', fz2, 'Color', color, 'EdgeColor', 'white');
hold on;
%breakyaxis([3 15]);


hold off