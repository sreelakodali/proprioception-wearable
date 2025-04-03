function [xIndices] = concatenateTrials(subjectN, cellArr)

l1 = 2;

testTotal = []; %zeros(sum(cell2mat(cellArr(:,3))),1);
graphIconTotal = [];
refArr = [];
xIndices = [];
newIdx = 0;
for i= 1:size(cellArr,1)
    newIdx = newIdx + cell2mat(cellArr(i,3));
    xIndices = [xIndices; newIdx];
    r = cell2mat(cellArr(i,4));
    x = cell2mat(cellArr(i,5));
    refLocal = r*ones(size(x));

    testTotal = [testTotal;x];
    graphIconTotal = [graphIconTotal;cell2mat(cellArr(i,6))];
    refArr = [refArr;refLocal];

end

figure;
set(gcf,'color','white');
ax = gca(gcf);
plot(0:length(testTotal)-1, testTotal, 'Color','#ea4335','Marker','x', 'LineWidth',l1, 'MarkerSize',10); hold on;
plot(0:length(testTotal)-1, refArr, 'Color', '#666666', 'LineStyle','--', 'LineWidth',l1); hold on;
plot(0:length(testTotal)-1,graphIconTotal, 'Color', '#00ff00', 'Marker', 'o', 'MarkerSize', 10, 'LineStyle','none', 'MarkerFaceColor','#00ff00'); hold on;
xlabel('Trials');
ylabel('Force (N)');
for j=1:length(xIndices)
    xline(xIndices(j),'-','LineWidth',l1*0.5, 'Color', '#666666'); hold on;
end

ylim(ax,[0,max(testTotal)]);
xlim(ax,[0,length(testTotal)]);
sg = title("Subject " + subjectN);
ax.FontSize = 18;
sg.FontWeight = 'bold';

end