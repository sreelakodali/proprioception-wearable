function [subjectN, JNDArr, JNDAbsArr] = plotAllTrialsGrid(subjectN, cellArr, cellPlotOrder, yMax, nTrials, coordinates)

%cellPlotOrder = [1, 2, 3, 4, 5, 6, 7, 8]; % 6, which order of data plotted
l1 = 2;

% coordinates = [1, 1, 1; 2, 1, 2; 3, 1, 3; 4, 2, 1; 5, 2, 2; 6, 2, 3; 7,
% 3, 1; 8, 3, 2; 9, 4, 1; 10, 4, 2]; % for subject 6, nTrials=3

%coordinates = [1, 1, 1; 2, 1, 2; 3, 2, 1; 4, 2, 2; 5, 3, 1; 6, 3, 2; 7, 4,
%1; 8, 4, 2]; % for subjects 7 and 8, nTrials=2


figure;
set(gcf,'color','white');
sg = sgtitle("Subject " + subjectN);
sg.FontSize = 18;
sg.FontWeight = 'bold';

% nSubject = str2num(subjectN);
% if (nSubject == 7)
%     cellPlotOrder = [5, 7, 6, 8, 1, 2, 3, 4]; % 7, which order of data plotted
% end

JNDArr = zeros(4,nTrials);
JNDAbsArr = zeros(4,nTrials);

for i= 1:size(cellArr,1)
    N = cellPlotOrder(i);
    s = subplot(2,2*nTrials,coordinates(i,1));
    plot(0:(cellArr{N,3}-1), cellArr{N,5}, 'Color','#ea4335','Marker','x', 'LineWidth',l1, 'MarkerSize',10); hold on;
    yline(cellArr{N,4},'--','LineWidth',l1, 'Color', '#666666'); hold on;
    plot(0:(cellArr{N,3}-1),cellArr{N,6}, 'Color', '#00ff00', 'Marker', 'o', 'MarkerSize', 10, 'LineStyle','none', 'MarkerFaceColor','#00ff00'); hold on;
    
    % compute PSE
    JND = cellArr{N,9};
    JND_abs = cellArr{N,10};
   % [JND, JND_abs] = computeJND(cellArr{N,5}, cellArr{N,4});

    row = coordinates(i,2);%1+floor((i-1)/nTrials);
    col = coordinates(i,3);%2-mod(i,2);
%     JNDArr(1+floor((i-1)/nTrials),2-mod(i,2)) = JND;
%     JNDAbsArr(1+floor((i-1)/nTrials),2-mod(i,2)) = JND_abs;

    JNDArr(row,col) = JND;
    JNDAbsArr(row,col) = JND_abs;

    disp(strcat(cellArr{N,2}, " JND=", string(JND), " JND_abs=", string(JND_abs)))
    title(strcat(cellArr{N,2}, " JND=", string(JND), " JND_abs=", string(JND_abs)));
    ylim(s,[0,yMax]);
    xlim(s,[0,cellArr{N,3}-1]);
    xlabel('Trials');
    ylabel('Force (N)');
    % s1.ylim(ax,[0,max(test)+1]);
    s.FontSize = 12;

    
end

end