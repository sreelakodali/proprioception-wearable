function [forceRef, dataPerTrial, allData] = selectData(file, peaks)

close all

color="#0C1446";%reversal
color2 = "#29A0B1";%staircase
color3 = "#FF9636"; %JND
color4 = "#190204"; %reference
color5 = "#4B8378";
color6 = "#DF362D";
color7 = "#880ED4";

j1 = 1;
sz1 = 5;
lw2 = 2;
lw1 = 1;

ref = 10.434782608695652;

path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/';
onePoke = readmatrix(strcat(path,file, '/processed_', file,'.csv'),'NumHeaderLines',1);
commandMM_1p = interp1([47, 139],[0, 20],onePoke(:,3));
measuredMM_1p = interp1([986, 100],[0, 20],onePoke(:,4));
force_1p = onePoke(:,5);
time = onePoke(:,1);
nTrials = onePoke(:,9);

% this is for 2024-01-30_20-21
%peaks = modifyBounds(peaks,[], [36],[],[2, 5, 10, 15, 18, 19, 22, 31, 44]);
% this is for 3-18
%peaks = modifyBounds(peaks,[], [],[],[24, 34]);
peaks = modifyBounds(peaks,[], [2, 3, 4, 5, 7, 10, 13, 16, 18, 26, 28, 33, 34, 35, 36, 42, 43, 44, 46 47, 50],[],[2, 3, 4, 5, 6, 7, 8, 10, 11, 18, 21, 22, 23, 25, 26, 28, 30, 33, 40, 42, 43, 44, 45, 46, 48]);

forceRef = [];
forcePerTrial = {};
cmd = {};
measuredPerTrial = {};
for i = 1:(length(unique(nTrials))-1)
    a = find(nTrials==i);
    b = a(end);
    a = a(1);
    a = a - 1;

    figure;
    set(gcf,'color','white')
    ax = gca(gcf);

    plot(time(a:b),commandMM_1p(a:b),'Color', color2, 'LineWidth',lw2); hold on;
    plot(time(a:b),measuredMM_1p(a:b), 'Color', color5, 'LineWidth',lw2); hold on;
    %plotSK_JND(time(a:b),onePokeCommandCut(a:b), [], color, 0, sz1, j1, lw1, lw2, 1, 0, []);

    xlabel('Trial Number')
    ylabel('Actuator Command (mm)')
    ax.FontSize = 15;
    title(sprintf("Trial # %i", i))
    
    maskF = zeros(size(force_1p));
    maskF([peaks(i,1):peaks(i,2), peaks(i,3):peaks(i,4)]) = 1;
    selectedDataF = maskF .* force_1p;

    yyaxis right
    ylabel("Force (N)", 'Color', color7)
    ax.YAxis(2).Color = color7;
    plot(time(a:b),force_1p(a:b), 'Color', color7, 'LineWidth',lw2); hold on;
    plotSK_JND(time(a:b),selectedDataF(a:b), [], color6, 0, sz1, j1, lw1, lw2, 1, 0, []);


    % this is per trial
    f1 = [force_1p(peaks(i,1):peaks(i,2))];
    m1 = [measuredMM_1p(peaks(i,1):peaks(i,2))];

    f2 = [force_1p(peaks(i,3):peaks(i,4))];
    m2 = [measuredMM_1p(peaks(i,3):peaks(i,4))];

    if (peaks(i,5) == ref)
        % add the values to reference 
        forceRef(end+1:end+length(f1)) = f1;
        
        forcePerTrial(end+1) = {f2};
        cmd(end+1) = {peaks(i,6)};
        measuredPerTrial(end+1) = {m2};
    elseif (peaks(i,6) == ref)
        forceRef(end+1:end+length(f2)) = f2;

        forcePerTrial(end+1) = {f1};
        cmd(end+1) = {peaks(i,5)};
        measuredPerTrial(end+1) = {m1};
    end

%     % compute average force, stdev, n
%     avgF1 = mean(force_1p(peaks(i,1):peaks(i,2)));
%     stdF1 = std(force_1p(peaks(i,1):peaks(i,2)));
%     nF1 = length(force_1p(peaks(i,1):peaks(i,2)));
%     %f1 = {force_1p(peaks(i,1):peaks(i,2))};
% 
%     avgF2 = mean(force_1p(peaks(i,3):peaks(i,4)));
%     stdF2 = std(force_1p(peaks(i,3):peaks(i,4)));
%     nF2 = length(force_1p(peaks(i,3):peaks(i,4)));
%     %f2 = {force_1p(peaks(i,3):peaks(i,4))};
% 
%     disp([avgF1, stdF1, nF1, avgF2, stdF2, nF2]);


end

dataPerTrial = [forcePerTrial; measuredPerTrial; cmd];

% how to go from per trial to across all time

sorted = sortrows(dataPerTrial',3);
u = unique(cell2mat(sorted(:,3)));
allData = cell(length(u),3);

for i = 1:(length(u))
    allData(i,3) = {u(i)};
    x = find(cell2mat(sorted(:,3)) == u(i));
    
    forceBuf = [];
    measuredBuf = [];
    for j = x
        forceBuf = [cell2mat(forceBuf); cell2mat(sorted(j,1))];
        measuredBuf = [cell2mat(measuredBuf); cell2mat(sorted(j,2))];
        % concatenate force and measured
    end
    allData(i,1) = {forceBuf};
    allData(i,2) = {measuredBuf};
    %disp(x);    
end



end