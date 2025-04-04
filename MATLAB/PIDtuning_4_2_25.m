% Sreela Kodali, kodali@stanford.edu
% PID TUNING Round 2 with kd
clear;
close all;

path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/';
dataDir = ["2025-04-03_16-46_p12_i30_d0.5_updatedPolyFit", "2025-04-03_16-58_p12_i30_d0.5_updatedPolyFitV2", "2025-04-03_17-07_p12_i30_d0.5_updatedPolyFitV3", "2025-04-03_17-19_p12_i30_d0.5_updatedPolyFitV4", "2025-04-03_17-26_p12_i30_d0.5_updatedPolyFitV5", "2025-04-03_17-32_p12_i30_d0.5_updatedPolyFitV5", "2025-04-03_17-52_p12_i30_d0.5_updatedPolyFitV7"];
%["2025-04-02_22-15_p12_i30_d0.4_scale7_setpt4", "2025-04-02_22-25_p12_i30_d0.5", "2025-04-02_22-31_p12_i30_d0.4", "2025-04-02_22-35_p12_i30_d0.4", "2025-04-02_22-42_p12_i30_d0.55", "2025-04-02_22-48_p12_i30_d0.5", "2025-04-02_22-52_p12_i30_d0.5", "2025-04-02_22-56_p12_i30_d0.5", "2025-04-02_23-02_p12_i30_d0.5", "2025-04-02_23-07_p12_i30_d0.5", "2025-04-02_23-14_p12_i30_d0.5"];
%["2025-04-02_18-32_p15_i30_d0_scale9",  "2025-04-02_19-04_p15_i30_d0_scale8_setpt4","2025-04-02_20-03_p15_i30_d0.5_scale7_setpt4","2025-04-02_20-07_p15_i30_d0.3_scale7_setpt4","2025-04-02_20-16_p15_i30_d0.2_scale8_setpt4", "2025-04-02_20-37_p12_i30_d0.3_scale7_setpt4", "2025-04-02_20-41_p18_i30_d0.3_scale7_setpt4", "2025-04-02_20-45_p12_i30_d0.5_scale7_setpt4", "2025-04-02_20-50_p12_i30_d0.4_scale7_setpt4"]; %[];
%"2025-04-02_18-46_p11_i36_d0_scale9_setpt4",
%"2025-04-02_18-55_p11_i36_d0_scale4.4_setpt4",  "2025-04-02_19-10_p15_i30_d1_scale8_setpt4", "2025-04-02_19-18_p15_i30_d1_scale9_setpt4", "2025-04-02_19-35_p15_i30_d1_scale4.5_setpt4", "2025-04-02_19-43_p15_i30_d0.5_scale4.5_setpt4", "2025-04-02_19-47_p15_i30_d0.5_scale6_setpt4", "2025-04-02_19-58_p15_i30_d0.5_scale6_setpt4", "2025-04-02_20-03_p15_i30_d0.5_scale7_setpt4", "2025-04-02_20-07_p15_i30_d0.3_scale7_setpt4", "2025-04-02_20-12_p15_i30_d0.2_scale7_setpt4", "2025-04-02_20-16_p15_i30_d0.2_scale8_setpt4"


"2025-04-02_20-03_p15_i30_d0.5_scale7_setpt4",
"2025-04-02_20-07_p15_i30_d0.3_scale7_setpt4",
"2025-04-02_20-16_p15_i30_d0.2_scale8_setpt4"


for d=dataDir
    fileName1 = 'raw_' + d +'.csv';
    device1Data = readmatrix(strcat(path,d,'/',fileName1));
    
    t1 = device1Data(:,1)/1000;
    t1 = t1 - t1(1);
    command1= device1Data(:,2);
    force1 = device1Data(:,3);
    actuatorCommand1 = device1Data(:,5);
    measured1= device1Data(:,6);
    idx = find(diff(command1) < 0);
    
    figure;
    set(gcf,'color','white');
    ax = gca(gcf);
    plot(t1, command1, 'LineWidth',1.2); hold on;
    plot(t1, force1, 'LineWidth',1.2); hold on;
    scatter(t1(idx), command1(idx), 'cyan', 'filled'); hold on;
    ax.FontSize = 18;
    %ylim([0,max(force1)]);
    xlabel("time (s)")
    ylabel("force (N)")
    yyaxis right
    plot(t1, actuatorCommand1, 'LineWidth',1.2); hold on;
end

setpoints = 1:10;
scaleFArr = [8.7, 8.2, 7.9, 7.5, 7.0, 5.7, 4.7, 3.8, 3.1, 2.2];

pFit = polyfit(setpoints,scaleFArr,4);
y1 = polyval(pFit,setpoints);

figure;
set(gcf,'color','white');
ax1 = gca(gcf);
scatter(setpoints,scaleFArr, 'filled'); hold on;
plot(setpoints, y1); hold on;
%         plot(dist2, breakpoint, 'Marker','square', 'LineStyle','none', 'MarkerFaceColor', '#391306', 'MarkerSize',10);
%         title(strcat("Calibration: Subject ", subjectN," Arm Stiffness F = kx"));
%         xlabel('Distance (mm)');
%         ylabel('Force (N)');
%         ylim(ax1,[0,max(force)+1]);
        ax1.FontSize = 15;
