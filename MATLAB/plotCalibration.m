
% Sreela Kodali, kodali@stanford.edu
% Reading Raw Data from Staircasing JND and plotting

function [dist2, force2, pFit] = plotCalibration(subjectN, calibrationDir, indices)

%idxUser = 4; % which calibration strand plotted
l1 = 2;
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/';

% read in only rows length of 2 or 3. store limits, and plot
if (length(calibrationDir) > 1)
    calibrationData = readmatrix(strcat(path,calibrationDir,'/','NEW_processed_device1_',calibrationDir,'.csv'));
    dist = calibrationData(:,1)*(27.0/4095.0);
    force = calibrationData(:,2);

    c = find(calibrationData(:,1)==20);
    disp(c);
%     disp(c(4));
%     disp(c(5));
%     if ~isempty(c)
%         if (idxUser>= length(c))
%             idx = c(end);
%             idx2 = length(force);
%         else
%             idx = c(idxUser);
%             idx2 = c(idxUser+1)-1;
%         end
        
        idx = indices(1,1);
        idx2 = indices(1,2);
        
        drift = force(idx); % force(1);
        idx = idx+20;
        dist2 = dist(idx:idx2); %dist;%
        force2= force(idx:idx2)-drift; %force-drift;%

        pFit = polyfit(dist2,force2-drift,1);
        y1 = polyval(pFit,dist2);

        
        
        breakpoint = force2 .* ischange(force2, 'linear');
        breakpoint(breakpoint==0) = -1;

        %disp(breakpoint);
        figure;
        set(gcf,'color','white');
        ax1 = gca(gcf);
        scatter(dist2,force2-drift, 'filled', 'MarkerFaceColor','#F7BEC0'); hold on;
        plot(dist2, y1, 'LineWidth',5, 'Color', '#AA1945', 'LineStyle','--'); hold on;
        plot(dist2, breakpoint, 'Marker','square', 'LineStyle','none', 'MarkerFaceColor', '#391306', 'MarkerSize',10);
        title(strcat("Calibration: Subject ", subjectN," Arm Stiffness F = kx"));
        xlabel('Distance (mm)');
        ylabel('Force (N)');
        ylim(ax1,[0,max(force)+1]);
        ax1.FontSize = 15;
    %end

end


end