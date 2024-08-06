close all

learning = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Data/Pilot2/averageLearningSpeed_ALL_S1-16_n2_n8_reshaped.csv','NumHeaderLines',0);

sz = 10;
lw2 = 2;
lw1 = 1.5;
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

    plotSK(1:10, learning(:,k+1), [], color(k), 0, sz, 0, lw1, lw2, 1, 0, []);
end
xlabel('Target angles (deg)')
% xticks([1:6]);
xticklabels({'180','165','150', '135', '120', '105', '90', '75', '60', '45'})
% xlim([40,181])
ylabel('Mean angle speed (deg/s)')
ax.FontSize = 18;

leg = legend('', '', 'T4.1: Ascending','','','T4.2: Partly Ascending Descending ', '','','T4.3: Random', '','','T4.4: Random');
set(leg, 'edgeColor','w', 'Location','southeast');