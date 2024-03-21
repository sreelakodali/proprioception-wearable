% Looking at JND study data 3
% Written by Sreela Kodali kodali@stanford.edu

close all
clear
color2 = "#75E6DA";%"#B00000";
color = "#189AB4";%"#189AB4"; %"#0000FF";%1/255*[231,188,188];
color3 = "#FF6584";
color4 = "#050A30";
lw = 1.5;
bw = 1;


A = [-3.00000000e+00*(20/(139-47)) -5.52336957e-01  2.23414935e-01 -5.05865683e-01 2.38946268e-01  2.30000000e+01;
0.00000000e+00*(20/(139-47)) -9.83193277e-03  1.02321829e-01 -1.09439776e-02 1.74103398e-01  1.70000000e+01;
5.00000000e+00*(20/(139-47))  9.31645503e-01  6.21250501e-02  8.72518519e-01 1.25845331e-01  9.00000000e+00];


plotData = A(:,[1,2]);
figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

label = categorical({'-3'; '0'; '5'});
nil = zeros(3,1);
b = bar(label, [plotData, nil], 'grouped', 'EdgeColor','none'); hold on;
set(b(1), 'FaceColor',color2, 'BarWidth', bw);
set(b(2), 'FaceColor',color);
xlabel('PWM Staircase Increments')
ylabel('Difference in Actuator Position (mm)')
ax.FontSize = 18;
ylim([-1.1,1.1])

[ngroups,nbars] = size([plotData, nil]);
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end

B = A(:,[3]) ./ sqrt(A(:,[6]));
B = [zeros(3,1), B, zeros(3,1)];
%B = [zeros(3,1), A(:,[3,5])];
 
er = errorbar(x', [plotData, nil], B, 'color', color4, 'linestyle', 'none', 'linewidth', lw); hold on;

nil2 = zeros(3,2);
yyaxis right
ylabel("Force (N)", 'Color', color3)
ax.YAxis(2).Color = color3;
b1 = bar(label, [nil2, A(:,[4])], 'grouped', 'EdgeColor','none'); hold on;
set(b1(3), 'FaceColor',color3, 'BarWidth', bw);
ylim([-1.1,1.1])


[ngroups,nbars] = size([nil2, A(:,[4])]);
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end

B = A(:,[5]) ./ sqrt(A(:,[6]));
B = [zeros(3,1), zeros(3,1), B];
%B = [zeros(3,1), A(:,[3,5])];
 
er = errorbar(x', [nil2, A(:,[4])], B, 'color', color4, 'linestyle', 'none', 'linewidth', lw, 'Marker','none'); hold on;

leg = legend('Commanded Position', 'Measured Position', '', '', '', '', '', '', 'Force');
set(leg, 'edgeColor','w', 'Location','northwest');