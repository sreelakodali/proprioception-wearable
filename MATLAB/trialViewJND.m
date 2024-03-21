function [] = trialViewJND(file)

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

% cut1 = 0;%13;
% cut2 = 0;

path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/';
onePoke = readmatrix(strcat(path,file, '/processed_', file,'.csv'),'NumHeaderLines',1);
commandMM_1p = interp1([47, 139],[0, 20],onePoke(:,3));
measuredMM_1p = interp1([986, 100],[0, 20],onePoke(:,4));
force_1p = onePoke(:,5);
time = onePoke(:,1);
nTrials = onePoke(:,9);


% edge detection
peaksC = edgeDetection(file,1);
peaksF = edgeDetection(file,3); % note: these peaks need to get converted bc they're the gradient peaks

% %minimum processing for edges
% onePokeCommandCut = abs(peaksC);
% peakMask = peaksF;
% peakMask(peakMask ~= 0) = 1;
% onePokeForceCut = peakMask .* force_1p;

% shift edges if need be
[idxPeakC_Rising, idxPeakC_Falling] = shiftPeaks(peaksC, 0, 0);
[idxPeakF_Rising, idxPeakF_Falling] = shiftPeaks(peaksF, 2, -1);

%criteria for valid window:
% both positive values, at least t seconds apart, rising and falling edge

data = [];
nSqr = 0;
minWindow = 1;
for i = 1:length(idxPeakC_Rising)
    check1 = idxPeakC_Rising(i) < idxPeakC_Falling(i);
    check2 = (sign(commandMM_1p(idxPeakC_Rising(i))) && sign(commandMM_1p(idxPeakC_Rising(i))));
    check3 = ((time(idxPeakC_Falling(i)) - time(idxPeakC_Rising(i))) > minWindow);

    if (check1 && check2 && check3)
        sqr = idxPeakC_Rising(i):idxPeakC_Falling(i);
         nSqr = nSqr + 1;
        data(end+1:end+length(sqr)) = sqr;
    end
end

% data = [];
% rising = 0;
% falling = 0;
% nSqr = 0;
% for i = 1:length(idxPeakC)
% 
%     x = idxPeakC(i);
%     %if valid square, add to data
% 
%     % rising edge 
%     if ((sign(peaksC(x)) > 0) && (falling == 0))
%         rising = x;
%     end
% 
%     if ((sign(peaksC(x)) < 0) && (sign(rising) == 1))
%         falling = x;
%          % we have a square, add to data
%         sqr = rising:falling;
%         nSqr = nSqr + 1;
%         
%         data(end+1:end+length(sqr)) = sqr;
%         rising = 0;
%         falling = 0;
%     end
% end
disp(nSqr);

selectedData = zeros(size(commandMM_1p));
selectedData(data) = 1;
selectedData = selectedData .* commandMM_1p;

% disp(length(idxPeakC))
% disp(length(idxPeakF))

peakMaskC = zeros(size(commandMM_1p));
peakMaskC([idxPeakC_Rising; idxPeakC_Falling]) = 1;
onePokeCommandCut = peakMaskC .* commandMM_1p;

peakMaskF = zeros(size(force_1p));
peakMaskF([idxPeakF_Rising; idxPeakF_Falling]) = 1;
onePokeForceCut = peakMaskF .* force_1p;

%for i = 1:10
for i = 1:(length(unique(nTrials))-1)
%i = 10;
    % first and last occurance of trial i
    a = find(nTrials==i);
    b = a(end);
    a = a(1);
    a = a - 1;

    figure;
    set(gcf,'color','white')
    ax = gca(gcf);
 
    plot(time(a:b),commandMM_1p(a:b),'Color', color2, 'LineWidth',lw2); hold on;
    plot(time(a:b),measuredMM_1p(a:b), 'Color', color5, 'LineWidth',lw2); hold on;
    plotSK_JND(time(a:b),onePokeCommandCut(a:b), [], color, 0, sz1, j1, lw1, lw2, 1, 0, []);
    plotSK_JND(time(a:b),selectedData(a:b), [], color6, 0, sz1, j1, lw1, lw2, 1, 0, []);
    xlabel('Two Contacts, Trial Number')
    ylabel('Actuator Command (mm)')
    ax.FontSize = 15;
    title(sprintf("Trial # %i", i))

    yyaxis right
    ylabel("Force (N)", 'Color', color7)
    ax.YAxis(2).Color = color7;
    plot(time(a:b),force_1p(a:b), 'Color', color7, 'LineWidth',lw2); hold on;
    plotSK_JND(time(a:b),onePokeForceCut(a:b), [], color, 0, sz1, j1, lw1, lw2, 1, 0, []);
    %ylim([0,10])
end
