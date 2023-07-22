% run skFig4 first

forceRange = plotData(:,2) - plotData(:,1);
forceRange = forceRange(1:14);
color = "#0093AC";
errABSPerSubject = [12.5,
12.6,
23.6,
15.2,
21.8,
14.8,
10.5,
21.6,
8.7,
17.2,
21.2,
10.1,
21.5,
9.5 ];

sz = 100;
figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

scatter(forceRange,errABSPerSubject, sz, "magenta",'filled');

xlabel('Force Range of a Subject (N)')
% xticks([1:6]);
% xticklabels({'180','165','150', '135', '120', '105', '90', '75', '60', '45'})
% xlim([40,181])
ylabel('Mean angle error (deg)')
ax.FontSize = 18;

mdl = fitlm(forceRange,errABSPerSubject)