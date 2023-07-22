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

color = "#0093AC";
color2 = "#91B5BB";%"#189AB4"; %"#0000FF";%1/255*[231,188,188];
j = 3;
sz = 10;
lw = 2;
flipBool = 0;

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);


x = angles;
y = F_avgHnV;
SEM = F_stdErrHnV;
disp(SEM)
if flipBool
    p = plot(x, flip(y), 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color); hold on;
    xi = [x(1):1:x(end)];
    vid=interp1(x,y,xi,'spline');
    p2 = plot(xi,flip(vid), ':'); hold on;
    xticklabels({'180','165','150', '135', '120', '105', '90', '75', '60', '45'})
else
    p = plot(x, y, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color); hold on;
    xi = [x(1):1:x(end)];
    vid=interp1(x,y,xi,'spline');
    p2 = plot(xi,vid, ':'); hold on;
    
end
e = errorbar(x,y,SEM,"o"); hold on;
e.Color = color;
e.LineWidth = 1;

p2.LineWidth = lw;
p2.Color = color;
xlim([40,180])


x2 = x-j;
y = F_avgnHnV;
SEM = F_stdErrnHnV;
if flipBool
    p = plot(x2, flip(y), 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2); hold on;
    vid2=interp1(x2+2*j,y,xi,'spline');
    p3 = plot(xi,flip(vid2), ':'); hold on;
else
    p = plot(x2, y, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2); hold on;
    vid2=interp1(x2,y,xi,'spline');
    p3 = plot(xi,vid2, ':'); hold on;
end
e2 = errorbar(x2,y,SEM,"o"); hold on;
e2.Color = color2;
e2.LineWidth = 1;
p3.LineWidth = lw;
p3.Color = color2;
%errorbar(x2,y,SEM,'b');
ylim([-1 5]);
xlabel('target angles (deg)')
ylabel('Force (N)')
%ylabel('angle mean absolute error (deg)')
ax.XTick = 45:15:180;
ax.FontSize = 18;
leg = legend('Haptic','','', 'No Haptic', '', '');
set(leg, 'edgeColor','w');