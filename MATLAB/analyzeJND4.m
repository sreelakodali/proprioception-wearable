% Looking at JND study data 2
% Written by Sreela Kodali kodali@stanford.edu

close all
clear
color="#0C1446";%reversal
color2 = "#29A0B1";%staircase
color3 = "#FF9636"; %JND
color4 = "#190204"; %reference
color5 = "#4B8378";
color6 = "#DF362D";
color7 = "#880ED4";


onePoke = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/2024-01-30_20-47/processed_2024-01-30_20-47.csv','NumHeaderLines',1);
twoPoke = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/2024-01-30_20-21/processed_2024-01-30_20-21.csv','NumHeaderLines',1);
twoPoke2 = twoPoke;

cut = 5;
cut1 = 5;
cut2 = 5;
j = 0.04;
sz = 50;
idx_remove = [];

for i = 1:(size(twoPoke,1)-1)
    if twoPoke(i,3) ~= twoPoke(i+1,3)
        %disp(twoPoke(i+1,3))
        idx_remove(end+1:end+cut+1) = i+1:i+1+cut;
    end
end
twoPoke(idx_remove,:) = [];
commandMM = interp1([47, 139],[0, 20],twoPoke(:,3));
measuredMM = interp1([986, 100],[0, 20],twoPoke(:,4));
force = twoPoke(:,5);


idx_remove1 = [];
for i = 1:(size(onePoke,1)-1)
    if onePoke(i,3) ~= onePoke(i+1,3)
        %disp(twoPoke(i+1,3))
        idx_remove1(end+1:end+cut1+1) = i+1:i+1+cut1;
    end
end
onePoke(idx_remove1,:) = [];
commandMM_1p = interp1([47, 139],[0, 20],onePoke(:,3));
measuredMM_1p = interp1([986, 100],[0, 20],onePoke(:,4));
force_1p = onePoke(:,5);


idx_remove2 = [];
for i = 1:(size(twoPoke2,1)-1)
    if twoPoke2(i,6) ~= twoPoke2(i+1,6)
        %disp(twoPoke(i+1,3))
        idx_remove2(end+1:end+cut2+1) = i+1:i+1+cut2;
    end
end
twoPoke2(idx_remove2,:) = [];
commandMM_2p = interp1([47, 139],[0, 20],twoPoke2(:,6));
measuredMM_2p = interp1([986, 100],[0, 20],twoPoke2(:,7));
force_2p = twoPoke2(:,8);
commandMM_2p(isnan(commandMM_2p))=0;

% figure;
% fig = gcf;
% set(gcf,'color','white')
% ax = gca(gcf); 
% 
% s1 = subplot(1,3,1);
% 
% yyaxis left
% scatter(commandMM_1p,measuredMM_1p,sz,commandMM_1p, 's', 'filled')
% colormap(s1, "winter");
% 
% % ylim([5,20])
% xlim([10,16])
% %xlim([90,120])
% xticks(round(unique(commandMM_1p),1))
% xlabel('One Contact, Actuator Command (mm)')
% ylabel('Actuator Position')
% s1.FontSize = 15;
% s1.XTickLabelRotation = 45;
% 
% 
% yyaxis right
% colormap("cool");
% scatter(commandMM_1p+j,force_1p,sz,commandMM_1p, 's', 'filled')
% ylabel("Force (N)", 'Color', "#880ED4")
% s1.YAxis(2).Color = "#880ED4";
% ylim([0,10])
% 
% 
% s2 = subplot(1,3,2);
% scatter(commandMM,measuredMM,sz,commandMM, 's', 'filled')
% %colormap(s2, "winter");
% 
% % ylim([5,20])
% xlim([10,16])
% %xlim([90,120])
% xticks(round(unique(commandMM),1))
% xlabel('Two Contacts: Actuator 1, Actuator Command (mm)')
% ylabel('Actuator Position')
% s2.FontSize = 15;
% s2.XTickLabelRotation = 45;
% 
% yyaxis right
% colormap("cool");
% scatter(commandMM+j,force,sz,commandMM, 's', 'filled')
% ylabel("Force (N)", 'Color', "#880ED4")
% s2.YAxis(2).Color = "#880ED4";
% ylim([0,10])
% 
% 
% s3 = subplot(1,3,3);
% scatter(commandMM_2p,measuredMM_2p,sz,commandMM_2p, 's', 'filled')
% %colormap(s2, "winter");
% 
% ylim([8,14])
% xlim([10,16])
% %xlim([90,120])
% xticks(round(unique(commandMM_2p),1))
% xlabel('Two Contacts: Actuator 2, Actuator Command (mm)')
% ylabel('Actuator Position')
% s3.FontSize = 15;
% s3.XTickLabelRotation = 45;
% 
% yyaxis right
% colormap("cool");
% scatter(commandMM_2p+j,force_2p,sz,commandMM_2p, 's', 'filled')
% ylabel("Force (N)", 'Color', "#880ED4")
% s3.YAxis(2).Color = "#880ED4";
% ylim([0,10])
% colormap(s3,"winter");
% colormap(s2,"winter");
% colormap(s1,"winter");

% %---------------------

% figure;
% fig = gcf;
% set(gcf,'color','white')
% ax = gca(gcf); 
% 
% 
% 
% s4 = subplot(1,3,1);
% b = boxchart(commandMM_1p,measuredMM_1p, 'BoxFaceColor',color2, 'MarkerColor',color2, 'MarkerStyle','o');
% b.JitterOutliers = 'on';
% b.BoxWidth = 0.2;
% b.LineWidth = 1.5;
% xlim([10,16])
% ylim([7,14])
% % ylim([5,20])
% %xlim([90,120])
% xticks(round(unique(commandMM_1p),1))
% xlabel('One Contact, Actuator Command (mm)')
% ylabel('Actuator Position')
% s4.FontSize = 15;
% s4.XTickLabelRotation = 45;
% 
% 
% yyaxis right
% % colormap("cool");
% % scatter(commandMM_1p+j,force_1p,sz,commandMM_1p, 's', 'filled')
% b = boxchart(commandMM_1p,force_1p, 'BoxFaceColor',color7, 'MarkerColor',color7, 'MarkerStyle','o');
% b.JitterOutliers = 'on';
% b.BoxWidth = 0.2;
% b.LineWidth = 1.5;
% ylabel("Force (N)", 'Color', color7)
% s4.YAxis(2).Color = color7;
% ylim([0,10])
% 
% 
% s5 = subplot(1,3,2);
% % scatter(commandMM,measuredMM,sz,commandMM, 's', 'filled')
% b = boxchart(commandMM,measuredMM, 'BoxFaceColor',color2, 'MarkerColor',color2, 'MarkerStyle','o');
% b.JitterOutliers = 'on';
% b.BoxWidth = 0.2;
% b.LineWidth = 1.5;
% % ylim([5,20])
% xlim([10,16])
% ylim([7,14])
% %xlim([90,120])
% xticks(round(unique(commandMM),1))
% xlabel('Two Contacts: Actuator 1, Actuator Command (mm)')
% ylabel('Actuator Position')
% s5.FontSize = 15;
% s5.XTickLabelRotation = 45;
% 
% yyaxis right
% % colormap("cool");
% % scatter(commandMM+j,force,sz,commandMM, 's', 'filled')
% b = boxchart(commandMM,force, 'BoxFaceColor',color7, 'MarkerColor',color7, 'MarkerStyle','o');
% b.JitterOutliers = 'on';
% b.BoxWidth = 0.2;
% b.LineWidth = 1.5;
% ylabel("Force (N)", 'Color', color7)
% s5.YAxis(2).Color = color7;
% ylim([0,10])
% 
% 
% s6 = subplot(1,3,3);
% %scatter(commandMM_2p,measuredMM_2p,sz,commandMM_2p, 's', 'filled')
% b = boxchart(commandMM_2p,measuredMM_2p, 'BoxFaceColor',color2, 'MarkerColor',color2, 'MarkerStyle','o');
% b.JitterOutliers = 'on';
% b.BoxWidth = 0.2;
% b.LineWidth = 1.5;
% %colormap(s2, "winter");
% 
% ylim([7,14])
% xlim([10,16])
% %xlim([90,120])
% xticks(round(unique(commandMM_2p),1))
% xlabel('Two Contacts: Actuator 2, Actuator Command (mm)')
% ylabel('Actuator Position')
% s6.FontSize = 15;
% s6.XTickLabelRotation = 45;
% 
% yyaxis right
% % colormap("cool");
% % scatter(commandMM_2p+j,force_2p,sz,commandMM_2p, 's', 'filled')
% b = boxchart(commandMM_2p,force_2p, 'BoxFaceColor',color7, 'MarkerColor',color7, 'MarkerStyle','o');
% b.JitterOutliers = 'on';
% b.BoxWidth = 0.2;
% b.LineWidth = 1.5;
% ylabel("Force (N)", 'Color', color7)
% s6.YAxis(2).Color = color7;
% ylim([0,10])

%----------------

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf); 

b = boxchart(commandMM_1p,measuredMM_1p, 'BoxFaceColor',color2, 'MarkerColor',color2, 'MarkerStyle','o');
b.JitterOutliers = 'on';
b.BoxWidth = 0.2;
b.LineWidth = 1.5;
%b = boxchart([commandMM_1p; commandMM_1p],[measuredMM_1p; force_1p], 'GroupByColor', [ones(size(measuredMM_1p)); zeros(size(force_1p))]);
%b.JitterOutliers = 'on';
% b(1).BoxWidth = 0.2;
% b(1).LineWidth = 1.5;
% b(2).BoxWidth = 0.2;
% b(2).LineWidth = 1.5;
xlim([10,16])
ylim([7,14])
% ylim([5,20])
%xlim([90,120])
xticks(round(unique(commandMM_1p),1))
xlabel('One Contact, Actuator Command (mm)')
ylabel('Actuator Position')
ax.FontSize = 15;
ax.XTickLabelRotation = 45;


yyaxis right
% colormap("cool");
% scatter(commandMM_1p+j,force_1p,sz,commandMM_1p, 's', 'filled')
b = boxchart(commandMM_1p,force_1p, 'BoxFaceColor',color7, 'MarkerColor',color7, 'MarkerStyle','o');
b.JitterOutliers = 'on';
b.BoxWidth = 0.2;
b.LineWidth = 1.5;
ylabel("Force (N)", 'Color', color7)
ax.YAxis(2).Color = color7;
ylim([0,10])