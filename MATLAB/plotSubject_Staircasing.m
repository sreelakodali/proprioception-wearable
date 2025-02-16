
% Sreela Kodali, kodali@stanford.edu
% Reading Raw Data from Staircasing JND and plotting

function [] = plotSubject_Staircasing(dataDir, nActArr, p)
close all;

calibrationDir = '';
% first 2 directories are nAct=2, last one is nAct=1
% dataDir = ["subject7_2025-02-12_20-53", "subject7_2025-02-12_21-17", "subject7_2025-02-12_22-02"];
% nActArr_2 = [1,2]; % which directory indices have 2 actuators activated
% nActArr = [2, 2, 1];
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/';

l1 = 2;
cellArr = {};
yMax = 0;

% % for each directory in dataDir, will read all the trial*.csv.
%  if data isn't empty then, plots it
for i = 1:length(dataDir)
    localPath = path + dataDir(i) + "/";
    listing = struct2table(dir(localPath+"trial*.csv"));
    nAct = nActArr(i);
     
    if (~isempty(listing.name))
        for j = 1:length(listing.name)

            localName = listing.name(j);
            data = readmatrix(strcat(localPath,localName));

            if (size(data,1) > 3)
                % plot data
                nTrials = data(:,1);
                test = data(:,2);
                localMax = max(test);
                if (localMax > yMax)
                    yMax = localMax;
                end
                ref = data(:,3);
                graphIcon = data(:,9);

                graphIcon(graphIcon==1) = -1;
                graphIcon(graphIcon==3) = 1;
                graphIconVals = test .* graphIcon;

                trialNumber = cell2mat(strfind(localName, 'trial'));
                localName = localName{:};
                trialNumber = localName(trialNumber+5);

                quartile = strfind(localName, '_q');
                quartile = localName(quartile+2);

                subjectN = strfind(localName, '_subject');
                subjectN = localName(subjectN+8);

                x = strcat(string(nAct), 'q', quartile, '_', trialNumber);
                %dataTitles = [dataTitles, x];

                localCell = {localName, x, length(nTrials), ref(1), test, graphIconVals, trialNumber, quartile};
                cellArr = [cellArr; localCell];
                
                
                %dict = insert(dict, strcat(nAct, "q", quartile, "_", trialNumber), localCell);
                if (p)
                figure;
                set(gcf,'color','white');
                ax = gca(gcf);
                plot(nTrials-1, test, 'Color','#ea4335','Marker','x', 'LineWidth',l1, 'MarkerSize',10); hold on;
                plot(nTrials-1, ref, 'Color', '#666666', 'LineStyle','--', 'LineWidth',l1); hold on;
                plot(nTrials-1,graphIconVals, 'Color', '#00ff00', 'Marker', 'o', 'MarkerSize', 10, 'LineStyle','none', 'MarkerFaceColor','#00ff00'); hold on;
                title(strcat("Subject ", subjectN, ": Q", quartile, " Trial #", trialNumber)); hold on;
                xlabel('Trials');
                ylabel('Force (N)');
                ylim(ax,[0,max(test)+1]);
                ax.FontSize = 15;
                end
                
            end
        end
    end
end


cellPlotOrder = [5, 7, 6, 8, 1, 2, 3, 4]; % default

figure;
set(gcf,'color','white');
sg = sgtitle("Subject " + subjectN);
sg.FontSize = 18;
sg.FontWeight = 'bold';

% s1 = subplot(4,2,1);
% N = 5;
% plot(0:(cellArr{N,3}-1), cellArr{N,5}, 'Color','#ea4335','Marker','x', 'LineWidth',l1, 'MarkerSize',10); hold on;
% yline(cellArr{N,4},'--','LineWidth',l1, 'Color', '#666666'); hold on;
% plot(0:(cellArr{N,3}-1),cellArr{N,6}, 'Color', '#00ff00', 'Marker', 'o', 'MarkerSize', 10, 'LineStyle','none', 'MarkerFaceColor','#00ff00'); hold on;
% title(cellArr{N,2}); hold on;
% ylim(s1,[0,max(cellArr{N,5})+1]);
% xlabel('Trials');
% ylabel('Force (N)');
% % s1.ylim(ax,[0,max(test)+1]);
% s1.FontSize = 12;

for i= 1:length(cellPlotOrder)
    s = subplot(2,4,i);
    N = cellPlotOrder(i);
    plot(0:(cellArr{N,3}-1), cellArr{N,5}, 'Color','#ea4335','Marker','x', 'LineWidth',l1, 'MarkerSize',10); hold on;
    yline(cellArr{N,4},'--','LineWidth',l1, 'Color', '#666666'); hold on;
    plot(0:(cellArr{N,3}-1),cellArr{N,6}, 'Color', '#00ff00', 'Marker', 'o', 'MarkerSize', 10, 'LineStyle','none', 'MarkerFaceColor','#00ff00'); hold on;
    disp(cellArr{N,2});
    title(cellArr{N,2});
    ylim(s,[0,yMax]);
    xlim(s,[0,cellArr{N,3}-1]);
    xlabel('Trials');
    ylabel('Force (N)');
    % s1.ylim(ax,[0,max(test)+1]);
    s.FontSize = 12;

end

end