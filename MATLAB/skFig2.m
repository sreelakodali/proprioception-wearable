close all
HnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/subjectAttempts_HnV_16.csv','NumHeaderLines',0);
HV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/subjectAttempts_HV_16.csv','NumHeaderLines',0);
nHnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/subjectAttempts_nHnV_16.csv','NumHeaderLines',0);
nHV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/subjectAttempts_nHV_16.csv','NumHeaderLines',0);
forceHnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/force_HnV_16.csv','NumHeaderLines',0);
forceHV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/force_HV_16.csv','NumHeaderLines',0);
forcenHnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/force_nHnV_16.csv','NumHeaderLines',0);
forcenHV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/force_nHV_16.csv','NumHeaderLines',0);

% HnV([2, 8],:) = [];
% HV([2, 8],:) = [];
% nHnV([2, 8],:) = [];
% nHV([2, 8],:) = [];
% 
% forceHnV([2, 8],:) = [];
% forceHV([2, 8],:) = [];
% forcenHnV([2, 8],:) = [];
% forcenHV([2, 8],:) = [];


F_avgHnV = mean(forceHnV,1);
F_stdErrHnV = std(forceHnV, 0, 1)/sqrt(length(forceHnV));

F_avgHV = mean(forceHV,1);
F_stdErrHV = std(forceHV, 0, 1)/sqrt(length(forceHV));

F_avgnHV = mean(forcenHnV, 1);
F_stdErrnHV = std(forcenHnV, 0, 1)/sqrt(length(forcenHnV)); 

F_avgnHnV = mean(forcenHV,1);
F_stdErrnHnV = std(forcenHV, 0, 1)/sqrt(length(forcenHV));

angles = 45:15:180;
for i = 1:10
    HnV(:,i) = abs(HnV(:,i) - angles(i));
    HV(:,i) = abs(HV(:,i) - angles(i));
    nHnV(:,i) = abs(nHnV(:,i) - angles(i));
    nHV(:,i) = abs(nHV(:,i) - angles(i));
end

avgHnV = mean(HnV,1);
stdErrHnV = std(HnV, 0, 1)/sqrt(length(HnV));

avgHV = mean(HV,1);
stdErrHV = std(HV, 0, 1)/sqrt(length(HV));

avgnHV = mean(nHV, 1);
stdErrnHV = std(nHV, 0, 1)/sqrt(length(nHV)); 

avgnHnV = mean(nHnV,1);
stdErrnHnV = std(nHnV, 0, 1)/sqrt(length(nHnV));

color = "#B00000";%"#B00000";
color2="#000000";%"#000000";%"#189AB4"; %"#0000FF";%1/255*[231,188,188];
color3 = "#FF2101";
j = 1;
sz = 10;
lw2 = 2;
lw1 = 1;

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);
c = flip(hot(100));


colorFactor = ceil(10*F_avgHnV);
cmap = zeros(10,3);
for i = 1:10
    cmap(i,:) = c(colorFactor(i)+36,:);
end
colormap(cmap);

plotSK(angles-j,avgnHnV, stdErrnHnV, color2, 0, sz, j, lw1, lw2, 1, 0, []);
plotSK(angles+j,avgHnV, stdErrHnV, color3, 0, sz, j, lw1, lw2, 1, 0, cmap);

plotSK(angles-j,avgnHV-0.5, stdErrnHV, color2, 1, sz, j, lw1, lw2, 1, 0, []);

plotSK(angles+j,avgHV+0.15, stdErrHV, color3, 1, sz, j, lw1, lw2, 1, 0, cmap);



xticklabels({'', '180','165','150', '135', '120', '105', '90', '75', '60', '45', ''})
 

xlim([40,182])


ylim([0 40]);
xlabel('Target angles (deg)')
ylabel('Mean of angle error magnitude (deg)')
%ylabel('angle mean absolute error (deg)')
ax.XTick = 30:15:195;
ax.FontSize = 18;


yyaxis right
ylabel("Force (N)", 'Color', 'black')
ylim([0,5])
set(ax, 'YColor', 'k');
leg = legend('','','No Haptic, No Visual','','', 'Haptic, No Visual', '','','No Haptic, Visual','','', 'Haptic, Visual', '', '');
set(leg, 'edgeColor','w', 'Location','northwest');
%colorbar