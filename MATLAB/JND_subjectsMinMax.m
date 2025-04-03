% Sreela Kodali, kodali@stanford.edu
% Reading Raw Data from Staircasing JND and plotting
close all;

path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/';
fileName = 'SpatialSummation_SubjectCalibrationData_S1-8.csv';
data = readmatrix(strcat(path,fileName));

colorArr = ["#FFD700", "#FFB14E", "#FA8775", "#EA5F94", "#CD34B5", "#9D02D7", "#0000FF"];

% figure;
% set(gcf,'color','white');
% ax = gca(gcf);
% x = [1, 2];
% colorArr = ["#FFD700", "#FFB14E", "#FA8775", "#EA5F94", "#CD34B5", "#9D02D7", "#0000FF"];
% for i = 1:size(data,1)
%     plot(x, data(i,11:12), 'Color', colorArr(i), 'Marker', 'o', 'MarkerSize',10, 'LineWidth',1.5, 'MarkerFaceColor',colorArr(i)); hold on;
% end
% xlim(ax, [0,3]);



% %colorArr5 = ["#90e0ef","#00b4d8","#0077b6","#03045e"]; %["#03045e","#0077b6","#00b4d8","#90e0ef"];
% colorArr5 = ["#caf0f8","#90e0ef","#00b4d8","#0077b6","#03045e"];
% figure;
% set(gcf,'color','white');
% ax = gca(gcf);
% for i = 1:size(data,1)
%     %plot(x2(i,:), data(i,11:12), 'Color', "#29A0B1", 'Marker', 'o', 'MarkerSize',8, 'LineWidth',2, 'MarkerFaceColor',"#29A0B1"); hold on;
%     plot(i*ones(1,2), data(i,11:12), 'Color', colorArr5(5), 'Marker', 'none','LineStyle', '-', 'LineWidth',1.5); hold on;
%     plot(i, data(i,11), 'Color', colorArr5(1), 'Marker', 'square', 'MarkerSize',8, 'MarkerFaceColor',colorArr5(1),'LineStyle', 'none'); hold on;
%     plot(i,  data(i,11) + (data(i,12) - data(i,11))/4, 'Color', colorArr5(2), 'Marker', 'square', 'MarkerSize',8, 'LineStyle', 'none', 'MarkerFaceColor',colorArr5(2)); hold on;
%     plot(i,  data(i,11) + (data(i,12) - data(i,11))/2, 'Color', colorArr5(3), 'Marker', 'square', 'MarkerSize',8, 'LineStyle', 'none', 'MarkerFaceColor',colorArr5(3)); hold on;
%     plot(i,  data(i,11) + 3*(data(i,12) - data(i,11))/4, 'Color', colorArr5(4), 'Marker', 'square', 'MarkerSize',8, 'LineStyle', 'none', 'MarkerFaceColor',colorArr5(4)); hold on;
%     plot(i, data(i,12), 'Color', colorArr5(5), 'Marker', 'square', 'MarkerSize',8, 'LineStyle', 'none', 'MarkerFaceColor',colorArr5(5)); hold on;
% 
% end
% xlabel('Subject #');
% ylabel('Force (N)');
% xlim(ax,[0.5,8.5]);
% ax.FontSize = 18;
% leg = legend('', 'Minimum Force','Q1', 'Q2', 'Q3', 'Maximum Force');
% set(leg, 'edgeColor','w', 'Location','northeast');

color2 = "#75E6DA";%"#B00000";
color = "#189AB4";%"#189AB4"; %"#0000FF";%1/255*[231,188,188];
color3 = "#05445E";
lw = 1.5;
bw = 1;
stdevMin = transpose(std(transpose(data(:,2:4)))/sqrt(3));
stdevMax = transpose(std(transpose(data(:,5:7)))/sqrt(3));


colorArr5 = ["#caf0f8","#90e0ef","#00b4d8","#0077b6","#004C86", "#03045e"];
figure;
set(gcf,'color','white');
ax = gca(gcf);
barData = zeros(size(data,1),5);

barData(:,1) = data(:,11);
barData(:,2) = (data(:,12) - data(:,11))/4;
barData(:,3) = (data(:,12) - data(:,11))/4;
barData(:,4) =(data(:,12) - data(:,11))/4; 
barData(:,5) = (data(:,12) - data(:,11))/4;


x2 = [ones(1,5)*1; ones(1,5)*2; ones(1,5)*3; ones(1,5)*4; ones(1,5)*5; ones(1,5)*6; ones(1,5)*7; ones(1,5)*8]; 
%x2 = [transpose(1:8) , transpose(1:8)];
b2 = bar(x2,barData, 'stacked', 'EdgeColor','none'); hold on; %'EdgeColor','#03045e', 'LineWidth', 0.75
set(b2(1), 'FaceColor','w', 'BarWidth', 0.5,  'EdgeColor','w'); hold on;
set(b2(2), 'FaceColor',colorArr5(1), 'BarWidth', 0.5); hold on;
set(b2(3), 'FaceColor',colorArr5(2), 'BarWidth', 0.5); hold on;
set(b2(4), 'FaceColor',colorArr5(3), 'BarWidth', 0.5); hold on;
set(b2(5), 'FaceColor',colorArr5(4), 'BarWidth', 0.5); hold on;
% for i = 1:size(data,1)
%     %plot(x2(i,:), data(i,11:12), 'Color', "#29A0B1", 'Marker', 'o', 'MarkerSize',8, 'LineWidth',2, 'MarkerFaceColor',"#29A0B1"); hold on;
%     plot(i*ones(1,2), data(i,11:12), 'Color', colorArr5(5), 'Marker', 'none','LineStyle', '-', 'LineWidth',1.5); hold on;
%     plot(i, data(i,11), 'Color', colorArr5(1), 'Marker', 'square', 'MarkerSize',8, 'MarkerFaceColor',colorArr5(1),'LineStyle', 'none'); hold on;
%     plot(i,  data(i,11) + (data(i,12) - data(i,11))/4, 'Color', colorArr5(2), 'Marker', 'square', 'MarkerSize',8, 'LineStyle', 'none', 'MarkerFaceColor',colorArr5(2)); hold on;
%     plot(i,  data(i,11) + (data(i,12) - data(i,11))/2, 'Color', colorArr5(3), 'Marker', 'square', 'MarkerSize',8, 'LineStyle', 'none', 'MarkerFaceColor',colorArr5(3)); hold on;
%     plot(i,  data(i,11) + 3*(data(i,12) - data(i,11))/4, 'Color', colorArr5(4), 'Marker', 'square', 'MarkerSize',8, 'LineStyle', 'none', 'MarkerFaceColor',colorArr5(4)); hold on;
%     plot(i, data(i,12), 'Color', colorArr5(5), 'Marker', 'square', 'MarkerSize',8, 'LineStyle', 'none', 'MarkerFaceColor',colorArr5(5)); hold on;
% 
% end
% [ngroups,nbars] = size([data(:,11); data(:,12)]);
% % Get the x coordinate of the bars
% z = nan(nbars, ngroups);
% z(1,:) = b2(1).XEndPoints;
% z(2,:) = b2(5).XEndPoints;
z = [transpose(1:8), transpose(1:8)];
er = errorbar(z, [data(:,11), data(:,12)], [stdevMin, stdevMax], 'color', color3, 'linestyle', 'none', 'linewidth', lw); hold on;
title("Allowable Stimulus Range for Deep Pressure")
xlabel('Subject #');
ylabel('Force (N)');
xlim(ax,[0.5,8.5]);
ax.FontSize = 18;
% leg = legend({'Minimum','.', '.', '.', 'Maximum'}, 'orientation', 'horizontal');
% set(leg, 'edgeColor','w', 'Location','northeast');





figure;
set(gcf,'color','white');
ax = gca(gcf);

barData2 = zeros(size(data,1),2);
%colorArr6 = ["#03045e","#023e8a","#0077b6","#0096c7","#00b4d8","#c5dbf0"];
colorArr6 = ["k","k","k","k","k","#c5dbf0"];
colorArr6 = flip(colorArr6);
%["#e6e5e0","#c5dbf0","#96b8db","#6083c5","#203590","#230462"];
%["#e9f5db","#cfe1b9","#b5c99a","#97a97c","#87986a","#718355"];
barData2(:,1) = data(:,11);
barData2(:,2) = (data(:,12) - data(:,11));
x3 = [ones(1,2)*1; ones(1,2)*2; ones(1,2)*3; ones(1,2)*4; ones(1,2)*5; ones(1,2)*6; ones(1,2)*7; ones(1,2)*8]; 
b2 = barh(x3,barData2, 'stacked', 'EdgeColor','none'); hold on;
set(b2(1), 'FaceColor','w', 'BarWidth', 0.5); hold on;
set(b2(2), 'FaceColor',colorArr6(1), 'BarWidth', 0.5, 'EdgeColor','#03045e'); hold on;
h = 18;
lw2 = 0.8;
m = '|';
for i = 1:size(data,1)
    %plot(x2(i,:), data(i,11:12), 'Color', "#29A0B1", 'Marker', 'o', 'MarkerSize',8, 'LineWidth',2, 'MarkerFaceColor',"#29A0B1"); hold on;
    %plot(i*ones(1,2), data(i,11:12), 'Color', colorArr5(5), 'Marker', 'none','LineStyle', '-', 'LineWidth',1.5); hold on;
    plot(data(i,11), i, 'Color', colorArr6(2), 'Marker', m, 'MarkerSize',h, 'LineStyle', 'none', 'LineWidth', lw2, 'MarkerFaceColor',colorArr6(2)); hold on;
    plot(data(i,11) + (data(i,12) - data(i,11))/4, i, 'Color', colorArr6(3), 'Marker', m, 'MarkerSize',h, 'LineWidth',lw2, 'LineStyle', 'none', 'MarkerFaceColor',colorArr6(3)); hold on;
    plot(data(i,11) + (data(i,12) - data(i,11))/2, i, 'Color', colorArr6(4), 'Marker', m, 'MarkerSize',h, 'LineWidth',lw2, 'LineStyle', 'none', 'MarkerFaceColor',colorArr6(4)); hold on;
    plot(data(i,11) + 3*(data(i,12) - data(i,11))/4, i,'Color', colorArr6(5), 'Marker', m, 'MarkerSize',h, 'LineWidth',lw2, 'LineStyle', 'none', 'MarkerFaceColor',colorArr6(5)); hold on;
    plot(data(i,12), i, 'Color', colorArr6(6), 'Marker', m, 'MarkerSize',h, 'LineWidth',lw2, 'LineStyle', 'none', 'MarkerFaceColor',colorArr6(6)); hold on;
end
xlabel('Force (N)')
ylabel('Subject #')
%ylim(ax,[0,10])
ax.FontSize = 18;
% leg = legend({'', '', 'Minimum','Q1', 'Q2', 'Q3', 'Maximum'}, 'orientation', 'horizontal');
% set(leg, 'edgeColor','w', 'Location','north');

% 
% [ngroups,nbars] = size(plotData);
% % Get the x coordinate of the bars
% z = nan(nbars, ngroups);
% for i = 1:nbars
%     z(i,:) = b(i).XEndPoints;
% end
% 
% 
% er = errorbar(z', plotData, [stdevMin, stdevMax], 'color', color3, 'linestyle', 'none', 'linewidth', lw); hold on;
% %er(1)(13).Color = 'w';
% %x = xline(15, ':', 'lineWidth', lw, 'Color',"#000000"); hold on;
% xticks(1:1:7);
% xticklabels({'1', '2','3','4', '5', '6', '7'})
% xtickangle(0)
% set(ax, 'TickLength', [0,0]);
% leg = legend('Minimum Force','Maximum Force');
% set(leg, 'edgeColor','w', 'Location','northeast');



colorArr2 = ["#ea9ba2","#83203e","#b8475d","#cdb9ae","#e6dcd7","#916e75","#ffffff"];
colorArr3 = ["#26ad84","#31e0ab","#04140f","#104736","#1b7a5d","#8dbdae","#c6ded7"];

colorIdx = [7:-1:1];
figure;
set(gcf,'color','white');
ax = gca(gcf);
for i = 1:7
    d = cell2mat(distCell(colorIdx(i)));
    f = cell2mat(forceCell(colorIdx(i)));

    breakpoint = f .* ischange(f, 'linear');
    breakpoint(breakpoint==0) = -1;

    pFit = polyfit(d-d(1),f-f(1),2);
    y1 = polyval(pFit,d-d(1));
    plot(d-d(1), f-f(1), 'Color', colorArr3(i), 'MarkerSize',5,'Marker', 'o', 'LineStyle','none', 'MarkerFaceColor',colorArr3(i)); hold on;
    %plot(d-d(1), breakpoint, 'Marker','o', 'LineStyle','none', 'MarkerFaceColor', 'none', 'MarkerSize',20, 'MarkerEdgeColor',colorArr3(i), 'LineWidth',5);

    %plot(d-d(1), y1, 'Color', colorArr3(i), 'LineWidth',2, 'LineStyle','-'); hold on;
end
leg = legend({'Subject 1','Subject 2','Subject 3','Subject 4','Subject 5','Subject 6','Subject 7', 'Subject 8'},'orientation', 'vertical');
set(leg, 'edgeColor','w', 'Location','southeast');
xlabel('Distance (mm)');
ylabel('Force (N)');
title("Force vs. Distance of Subjects' Forearms")
ax.FontSize = 18;
ylim(ax,[0,20]);
xlim(ax,[0,22]);

%colorArr4 = ["#000070", "#7678ed","#E0D8FF"];
colorArr4 = ["#E0D8FF", "#7678ed","#000070"];
figure;
set(gcf,'color','white');
ax = gca(gcf);

plotData2 = [2.54*data(2:end,8), 2.54*data(2:end,10), zeros(7,1)];
b = bar(plotData2, 'grouped', 'EdgeColor','none'); hold on;
set(b(1), 'FaceColor',colorArr4(1), 'BarWidth', bw);
set(b(2), 'FaceColor',colorArr4(2), 'BarWidth', bw);
set(b(3), 'FaceColor',"#ffffff", 'BarWidth', bw);
t = ylabel('Forearm Measurements (cm)');
yyaxis right
b1 = bar( [zeros(7,2), transpose(cell2mat(pCell)) * 1/.0254], 'grouped', 'EdgeColor','none'); hold on;
set(b1(1), 'FaceColor','#ffffff', 'BarWidth', bw);
set(b1(2), 'FaceColor','#ffffff', 'BarWidth', bw);
set(b1(3), 'FaceColor',colorArr4(3), 'BarWidth', bw);
ylabel('Mean Stiffness (N/m)', 'Color', 'k');
xlabel('Subject Number')
ax.FontSize = 18;
t.Color = colorArr4(2);
ax.YAxis(1).Color = colorArr4(2);
ax.YAxis(2).Color = 'k';
title("Forearm Measurements");
%ax.Color = colorArr4(2);
leg = legend({'Length','Diameter','', '', '', 'Stiffness'},'orientation', 'horizontal');
set(leg, 'edgeColor','w', 'Location','north');


% figure;
% set(gcf,'color','white');
% ax = gca(gcf);
% for i = 1:6
%     pk = cell2mat(pCell(i));
%     plot(data(i+1,9), data(i+1,10), 'Color', 'b','MarkerSize',5,'Marker', 'o', 'LineStyle','none', 'MarkerFaceColor','b'); hold on;
%     %plot(pk(1), data(i+1,12) - data(i+1,11), 'MarkerSize',10,'Marker', 'o', 'LineStyle','none', 'LineWidth',5); hold on;
% end
% xlabel('Arm Measurement (inch)');
% ylabel('ASR (N)');
% ax.FontSize = 15;
%ylim(ax,[0,20]);

% figure;
% set(gcf,'color','white');
% ax = gca(gcf);
% x3 = [x2, x2, x2];
% colorArr = ["#FFD700", "#FFB14E", "#FA8775", "#EA5F94", "#CD34B5", "#9D02D7", "#0000FF"];
% for i = 1:size(data,1)
%     plot(x3(i,:), data(i,2:7), 'Color', colorArr(i), 'Marker', 'o', 'MarkerSize',10, 'LineWidth',1.5, 'MarkerFaceColor',colorArr(i)); hold on;
% end
