
% Sreela Kodali, kodali@stanford.edu
% Reading Raw Data from Staircasing JND and plotting

function [subjectN, cellArr, yMax] = plotAllTrials(dataDir, nActArr, p)
%close all;

%calibrationDir = 'subject7_2025-02-12_20-40';
% first 2 directories are nAct=2, last one is nAct=1
% dataDir = ["subject7_2025-02-12_20-53", "subject7_2025-02-12_21-17", "subject7_2025-02-12_22-02"];
% nActArr_2 = [1,2]; % which directory indices have 2 actuators activated
% nActArr = [2, 2, 1];
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/';
l1 = 2;
cellArr = {};
yMax = 0;
counter = 0;

% % for each directory in dataDir, will read all the trial*.csv.
%  if data isn't empty then, plots it
for i = 1:length(dataDir)
    localPath = path + dataDir(i) + "/";
    listing = struct2table(dir(localPath+"trial*.csv"));
    listing = sortrows(listing, 'date');
    %disp(listing);

    if (size(listing.name,1) == 1) 
        listing.name = [string(listing.name)];
        %disp(size(listing.name));
    end

    if (~isempty(listing.name))
        
        for j = 1:length(listing.name)

%             % FIX: Temporary for subject 6 with all files in same directory
%             if j > 4
%                 nAct = 2;
%             end
            localName = listing.name(j);
            %disp(localName);
            data = readmatrix(strcat(localPath,localName));

            if (size(data,1) > 3)

                %valid file
                counter = counter + 1;
                nAct = nActArr(counter);
                % plot data
                nTrials = data(:,1);
                test = data(:,2);
                localMax = max(test);
                if (localMax > yMax)
                    yMax = localMax;
                end
                ref = data(:,3);
                graphIcon = data(:,9);
                reversals = data(:,8);
                reversals = [0; diff(reversals)];
                reversals(reversals==0) = -1;
                reversals = reversals .* test;

                graphIcon(graphIcon==1) = -1;
                graphIcon(graphIcon==3) = 1;
                graphIconVals = test .* graphIcon;

                trialNumber = strfind(localName, 'trial');
                %disp(class(trialNumber));
                if (class(trialNumber)=="cell")
                    trialNumber = cell2mat(trialNumber);
                end
                localName = localName{:};
                trialNumber = localName(trialNumber+5);

                quartile = strfind(localName, '_q');
                quartile = localName(quartile+2);

                subjectN = strfind(localName, '_subject');
                subjectN = localName(subjectN+8);

                x = strcat(string(nAct), 'q', quartile, '_', trialNumber);
                %dataTitles = [dataTitles, x];

                % compute PSE
                [JND, JND_abs, pse, pse_abs] = computeJND(test, ref(1));

                localCell = {localName, x, length(nTrials), ref(1), test, graphIconVals, trialNumber, quartile, JND, JND_abs};
                cellArr = [cellArr; localCell];
                y = strcat(x, " PSE=", string(pse), " PSE_abs=", string(pse_abs));
                %disp(y);


                %dict = insert(dict, strcat(nAct, "q", quartile, "_", trialNumber), localCell);
                if (p)
                figure;
                set(gcf,'color','white');
                ax = gca(gcf);
                plot(nTrials-1, test, 'Color','#ea4335','Marker','x', 'LineWidth',l1, 'MarkerSize',10); hold on;
                plot(nTrials-1, ref, 'Color', '#666666', 'LineStyle','--', 'LineWidth',l1); hold on;
                plot(nTrials-1,graphIconVals, 'Color', '#00ff00', 'Marker', 'o', 'MarkerSize', 10, 'LineStyle','none', 'MarkerFaceColor','#00ff00'); hold on;
                plot(nTrials-1,reversals, 'Color', '#666666', 'Marker', 'o', 'MarkerSize', 20, 'LineStyle','none', 'LineWidth',l1); hold on;
                title(strcat("Subject ", subjectN, ": ", y)); hold on;
                xlabel('Trials');
                ylabel('Force (N)');
                ylim(ax,[0,max(test)+1]);
                xlim(ax,[0,max(nTrials-1)]);
                ax.FontSize = 15;
                end
                
            end
        end
    end
end

end