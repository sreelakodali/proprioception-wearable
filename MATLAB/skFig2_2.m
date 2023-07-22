close all
HnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/subjectAttempts_HnV.csv','NumHeaderLines',0);
HV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/subjectAttempts_HV.csv','NumHeaderLines',0);
nHnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/subjectAttempts_nHnV.csv','NumHeaderLines',0);
nHV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/subjectAttempts_nHV.csv','NumHeaderLines',0);
forceHnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/force_HnV.csv','NumHeaderLines',0);
forceHV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/force_HV.csv','NumHeaderLines',0);
forcenHnV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/force_nHnV.csv','NumHeaderLines',0);
forcenHV = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/force_nHV.csv','NumHeaderLines',0);

F_avgHnV = mean(forceHnV,1);
F_stdErrHnV = std(forceHnV, 0, 1)/sqrt(14);

F_avgHV = mean(forceHV,1);
F_stdErrHV = std(forceHV, 0, 1)/sqrt(14);

F_avgnHV = mean(forcenHnV, 1);
F_stdErrnHV = std(forcenHnV, 0, 1)/sqrt(14); 

F_avgnHnV = mean(forcenHV,1);
F_stdErrnHnV = std(forcenHV, 0, 1)/sqrt(14);

angles = 45:15:180;
for i = 1:10
    HnV(:,i) = abs(HnV(:,i) - angles(i));
    HV(:,i) = abs(HV(:,i) - angles(i));
    nHnV(:,i) = abs(nHnV(:,i) - angles(i));
    nHV(:,i) = abs(nHV(:,i) - angles(i));
end

avgHnV = mean(HnV,1);
stdErrHnV = std(HnV, 0, 1)/sqrt(14);

avgHV = mean(HV,1);
stdErrHV = std(HV, 0, 1)/sqrt(14);

avgnHV = mean(nHV, 1);
stdErrnHV = std(nHV, 0, 1)/sqrt(14); 

avgnHnV = mean(nHnV,1);
stdErrnHnV = std(nHnV, 0, 1)/sqrt(14);

color = "#FF2101";%"#B00000";
color2 = "#000000";%"#91B5BB";%"#000000";%"#189AB4"; %"#0000FF";%1/255*[231,188,188];
color3 = "#E9D8E1";
j = 1;
sz = 10;
lw2 = 2;
lw1 = 1.5;

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);
% 
% plotSK(angles-j,avgnHnV, stdErrnHnV, color2, 0, sz, j, lw1, lw2, 1, 0, []);
% plotSK(angles-j,avgnHV, stdErrnHV, color2, 1, sz, j, lw1, lw2, 1, 0, []);
% plotSK(angles,avgHnV, stdErrHnV, color, 0, sz, j, lw1, lw2, 1, 0, []);
% plotSK(angles,avgHV, stdErrHV, color, 1, sz, j, lw1, lw2, 1, 0, []);
% xticklabels({'', '180','165','150', '135', '120', '105', '90', '75', '60', '45', ''})
% 
% xlim([40,180])
% ylim([0 50]);
% xlabel('Target angles (deg)')
% ylabel('Mean angle error (deg)')
% ylabel('angle mean absolute error (deg)')
% ax.XTick = 30:15:195;
% ax.FontSize = 18;


% figure;
% fig2 = gcf;
% set(fig2,'color','white')
% ax2 = gca(fig2);

plotSK(angles-j,abs(F_avgnHnV), F_stdErrnHnV, color2, 0, sz, j, lw1, lw2, 1, 0, []);
plotSK(angles-j,F_avgHnV, F_stdErrHnV, color, 0, sz, j, lw1, lw2, 1, 0, []);
plotSK(angles+j,abs(F_avgnHV), F_stdErrnHV, color2, 1, sz, j, lw1, lw2, 1, 0, []);
plotSK(angles+j,F_avgHV, F_stdErrHV, color, 1, sz, j, lw1, lw2, 1, 0, []);

ax.XTick = 30:15:195;
xticklabels({'', '180','165','150', '135', '120', '105', '90', '75', '60', '45', ''})
xlim([40,181])
ylim([0 6]);
xlabel('Target angles (deg)')
ylabel("Force (N)", 'Color', 'black')
ax.FontSize = 18;

yyaxis right
ylabel("Pressure (kPa)", 'Color', 'black')
ylim([0,34])
% 
% yyaxis right
% ylabel("Force (N)", 'Color', 'black')
% ylim([0,5])
set(ax, 'YColor', 'k');
leg = legend('', '', 'No Haptic, No Visual','','','Haptic, No Visual', '', '', 'No Haptic, Visual','','','Haptic, Visual');
set(leg, 'edgeColor','w', 'Location','northwest');
%colorbar