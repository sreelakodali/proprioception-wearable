close all

learning = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Data/Pilot2/averageLearning_ALL_S1-16_n2_n8.csv','NumHeaderLines',0);
learning(10,2) = 0.1;
black = "#000000";

cmp = winter(10);
cmp = floor(cmp*255);
color = ["", "", "", "", "", "", "", "", "", ""];
for i = 1:10
    color(i) = rgb2hex(cmp(i,:));
end

color = ["#000000", "#FF2101", "#E9D8E1", "#B00000", "#91B5BB", "#189AB4", "#0000FF", "#75E6DA", "#189AB4", "#05445E"];
color = ["#ffd700", "#ffb14e", "#fa8775", "#ea5f94", "#cd34b5", "#9d02d7","#0000ff", "#000000", "#000000", "#000000"];
sz = 10;
lw2 = 2;
lw1 = 1.5;

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

%plotSK(1:6, learning(10,2:end), [], color(10), 0, sz, j, lw1, lw2, 0, 0, []);

for k=1:size(learning,1)
    plotSK(1:6, learning(k,2:end), [], color(k), 0, sz, 0, lw1, lw2, 0, 0, []);
end
xlabel('Learning Stages')
xticks([1:6]);
xticklabels({'Visual', 'Visual','No V','No V', 'No V', 'No V'})
ylabel('Mean angle error (deg)')
ax.FontSize = 18;

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

for k=1:size(learning,1)
    plotSK(k*ones(size(learning,2)-1, 1), learning(k,2:end), [], color(k), 0, sz, 0, lw1, lw2, 0, 0, []);
    %plotSK(1:10, learning(:,k+1), [], color(k), 0, sz, 0, lw1, lw2, 0, 0, []);
end
xlabel('Target angles (deg)')
% xticks([1:6]);
xticklabels({'180','165','150', '135', '120', '105', '90', '75', '60', '45'})
% xlim([40,181])
ylabel('Mean angle error (deg)')
ax.FontSize = 18;


cmp = winter(4);
cmp = floor(cmp*255);
color = ["", "", "", "", "", ""];
for i = 1:length(cmp)
    color(i) = rgb2hex(cmp(i,:));
end

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

for k=1:(size(learning,2)-1)
    %disp(k);
    %plotSK(k*ones(size(learning,2)-1, 1), learning(k,2:end), [], color(k), 0, sz, 0, lw1, lw2, 0, 0, []);
    if or(k == 1, k == 2)
        plotSK(1:10, learning(:,k+1), [], black, 1, sz, 0, lw1, lw2, 0, 0, []);
    else
        plotSK(1:10, learning(:,k+1), [], color(k-2), 0, sz, 0, lw1, lw2, 0, 0, []);
    end
end
xlabel('Target angles (deg)')
% xticks([1:6]);
xticklabels({'180','165','150', '135', '120', '105', '90', '75', '60', '45'})
% xlim([40,181])
ylabel('Mean angle error (deg)')
ax.FontSize = 18;

leg = legend('', '', 'T2: Haptic, Visual','','','', '', '', 'T4.1: Ascending','','','T4.2: Pseudorandom', '','','T4.3: Random', '','','T4.4: Random');
set(leg, 'edgeColor','w', 'Location','northeast');

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);
learning3 = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Data/Pilot2/averageLearningSpeed_ALL_S1-16_n2_n8_reshaped.csv','NumHeaderLines',0);
learning4 = mean(learning3);
learning4 = learning4(2:end);
color1 = "#FF8882";
color2= "#8D3A69";
color3 = "#05445E";

z = zeros(4,1);
learning2 = mean(learning);
learning2 = learning2(4:end);

%bar([learning2', learning4']);

b = bar([learning2', z],'FaceColor',color1 , 'EdgeColor',[1 1 1]);hold on;
xlabel('Block # During Practice Phase')
xticks(1:4);
xticklabels({'1','2', '3', '4'})
ylabel('Mean of angle error magnitude (deg)')
ax.FontSize = 18;

[ngroups,nbars] = size(zeros(4, 1));
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end



er = errorbar(x', learning2, stdErr_err, 'color', color3, 'linestyle', 'none', 'linewidth', lw1);hold on;

yyaxis right


b2 = bar([z, learning4'],'FaceColor',color2,'EdgeColor',[1 1 1]);hold on;
ylabel("Completion Speed (deg/s)", 'Color', 'black')
ylim([0,7])
set(ax, 'YColor', 'k');

 
[ngroups,nbars] = size(zeros(4, 2));
% Get the x coordinate of the bars
x2 = nan(nbars, ngroups);
for i = 1:nbars
    x2(i,:) = b2(i).XEndPoints;
end
er2 = errorbar((x2(2,:))', learning4, stdErr_t, 'color', color3, 'linestyle', 'none', 'linewidth', lw1);hold on;

leg = legend('Error', '', '', 'Speed', '');
set(leg, 'edgeColor','w', 'Location','northwest');

% figure;
% fig = gcf;
% set(gcf,'color','white')
% ax = gca(gcf);
% bar(learning2, 'EdgeColor',[1 1 1]);
% xlabel('Learning Stages')
% xticks(1:4);
% xticklabels({'T4.1','T4.2', 'T4.3', 'T4.4'})
% ylabel('Mean angle error (deg)')
% ax.FontSize = 18;
% 
% figure;
% fig = gcf;
% set(gcf,'color','white')
% ax = gca(gcf);
% bar(learning4, 'EdgeColor',[1 1 1]);
% xlabel('Learning Stages')
% xticks(1:4);
% xticklabels({'T4.1','T4.2', 'T4.3', 'T4.4'})
% ylabel('Speed (deg)')
% ax.FontSize = 18;

% figure;
% fig = gcf;
% set(gcf,'color','white')
% ax = gca(gcf);
% 
% 
% tiledlayout(2,1)
% 
% ax1 = nexttile;
% bar(learning2, 'FaceColor', color1,'EdgeColor',[1 1 1]);
% ylabel('Mean angle error (deg)')
% xticks(1:4);
% xticklabels({'T4.1','T4.2', 'T4.3', 'T4.4'})
% 
% ax2 = nexttile;
% bar(learning4, 'FaceColor', color2,'EdgeColor',[1 1 1]);
% ylabel("Speed (deg/s)")
% ylim([0,5])
% 
% xlabel('Learning Stages')
% xticks(1:4);
% xticklabels({'T4.1','T4.2', 'T4.3', 'T4.4'})
% ax1.FontSize = 18;
% ax2.FontSize = 18;