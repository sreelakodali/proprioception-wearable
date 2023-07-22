% close all
clc

% separate test data by test case for all subjects
test1 = [];
test1Row = 1;
test2 = [];
test2Row = 1;
test3 = [];
test3Row = 1;
test4 = [];
test4Row = 1;

% Matrix M contains all test data from each subject (i.e. 40 rows per
% subject)

for i = 1:size(M_new,1)

    if M_new(i,5) == 1 % if test case 1 (H, NV)
        % select row, add to test1
        selectRow = M_new(i,:);
        test1(test1Row, :) = selectRow;
        test1Row = test1Row + 1;
    end

    if M_new(i,5) == 2 % if test case (H, V)
        % select row, add to test2 
        selectRow = M_new(i,:);
        test2(test2Row, :) = selectRow;
        test2Row = test2Row + 1;
    end

    if M_new(i,5) == 3 % if test case 3 (NH, NV)
        % select row, add to test3
        selectRow = M_new(i,:);
        test3(test3Row, :) = selectRow;
        test3Row = test3Row + 1;
    end

    if M_new(i,5) == 4 % if test case 4 (NH, V)
        % select row, add to test4 
        selectRow = M_new(i,:);
        test4(test4Row, :) = selectRow;
        test4Row = test4Row + 1;
    end

end

% calculate mean error and st dev for each test case
meanColumns1 = mean(test1,1);
meanAngleError1 = meanColumns1(4)
stdColumns1 = std(test1,1);
stdAngleError1 = stdColumns1(4);

meanColumns2 = mean(test2,1);
meanAngleError2 = meanColumns2(4)
stdColumns2 = std(test2,1);
stdAngleError2 = stdColumns2(4);

meanColumns3 = mean(test3,1);
meanAngleError3 = meanColumns3(4)
stdColumns3 = std(test3,1);
stdAngleError3 = stdColumns3(4)

meanColumns4 = mean(test4,1);
meanAngleError4 = meanColumns4(4)
stdColumns4 = std(test4,1);
stdAngleError4 = stdColumns4(4)

%% Section 1 Angle Errors for 4 Test Cases
x = categorical({'H, NV', 'NH, NV', 'H, V', 'NH, V'});
x = reordercats(x,{'H, NV', 'NH, NV', 'H, V', 'NH, V'});
y = [meanAngleError1 meanAngleError3 meanAngleError2 meanAngleError4];
SEM = [stdAngleError1 stdAngleError3 stdAngleError2 stdAngleError4];
% figure;
% bar(y); 
% sigstar({[1,2]},[0.05]);
% hold on;
% errorbar(y,SEM);
% ylabel('angle mean absolute error (deg)');
% xlabel('test condition');
% dim = [.5 .1 .1 .1];
% str = '1: H, NV, 2: NH, NV, 3: H, V, 4: NH, V';
% annotation('textbox',dim,'String',str)

x = categorical({'H, NV', 'NH, NV', 'H, V', 'NH, V'});
x = reordercats(x,{'H, NV', 'NH, NV', 'H, V', 'NH, V'});
y = [test1(:,4) test3(:,4) test2(:,4) test4(:,4)]
% SEM = [stdAngleError1 stdAngleError3 stdAngleError2 stdAngleError4];
% figure;
% swarmchart(x,y)
% hold on;
% % errorbar(y,SEM);
% ylabel('angle mean absolute error (deg)');
% xlabel('test condition');
% dim = [.5 .1 .1 .1];
% str = '1: H, NV, 2: NH, NV, 3: H, V, 4: NH, V';
% annotation('textbox',dim,'String',str)

% figure;
% x = categorical({'H, NV', 'NH, NV', 'H, V', 'NH, V'});
% x = reordercats(x,{'H, NV', 'NH, NV', 'H, V', 'NH, V'});
% y = [test1(:,4) test3(:,4) test2(:,4) test4(:,4)]
% isout = isoutlier(y,'quartiles');
% yClean = y;
% yClean(isout) = NaN;
% boxplot(yClean,'Notch','on','Labels',{'H, NV', 'NH, NV', 'H, V', 'NH, V'})
% ylabel('angle absolute error (deg)');
% xlabel('test condition');

x = categorical({'H, NV', 'NH, NV'});
x = reordercats(x,{'H, NV', 'NH, NV'});
y = [meanAngleError1 meanAngleError3];
SEM = [stdAngleError1 stdAngleError3];
% figure;
% bar(x,y); hold on;
% errorbar(y,SEM);
% ylabel('angle mean absolute error (deg)')
% xlabel('test condition')
% 
% x = categorical({'H, V', 'NH, V'});
% x = reordercats(x,{'H, V', 'NH, V'});
% y = [meanAngleError2 meanAngleError4];
% SEM = [stdAngleError2 stdAngleError4];
% figure;
% bar(x,y); hold on;
% % errorbar(y,SEM);
% ylabel('angle mean absolute error (deg)')
% xlabel('test condition')

%% Section 2 Errors vs. Angles

% create vectors to store errors for each test case each target angle
% create variables to store average of errors for each test case each
% target angle
for test_case = 1:4
    for angle = 45:15:180
        my_field = strcat('test',num2str(test_case),'_',num2str(angle));
        variable.(my_field) = [];
        my_field = strcat('test',num2str(test_case),'_',num2str(angle),'_avg');
        variable.(my_field) = 0;
        my_field = strcat('test',num2str(test_case),'_',num2str(angle),'_std');
        variable.(my_field) = 0;
    end
end

% populate those vectors with the actual error values
for i = 1:size(M_new,1) % loop through all rows of M
    
    for test_case = 1:4 % loop through test cases 1-4

        for angle = 45:15:180 % loop through all ten target angles

            if M_new(i,5) == test_case && M_new(i,2) == angle % if you are at the right test case (1-4) and target angle row
                
                selectVal = M_new(i,4); % select the absolute error value of that row
                my_field = strcat('test',num2str(test_case),'_',num2str(angle));
                variable.(my_field) = [variable.(my_field);selectVal]
                avg_field = strcat('test',num2str(test_case),'_',num2str(angle),'_avg');
                variable.(avg_field) = mean(variable.(my_field));
                std_field = strcat('test',num2str(test_case),'_',num2str(angle),'_std');
                variable.(std_field) = std(variable.(my_field));
            end

        end
    end

end

% create vectors to store test{test_case}_{angle}_avg values for each test
variable.test1_avg = []; variable.test2_avg = []; variable.test3_avg = []; variable.test4_avg = [];
variable.test1_std = []; variable.test2_std = []; variable.test3_std = []; variable.test4_std = [];

% populate those vectors with the average or std error for each target
% angle
for test_case = 1:4

    for angle = 45:15:180
        
        field = strcat('test',num2str(test_case),'_avg');
        avg_field = strcat('test',num2str(test_case),'_',num2str(angle),'_avg');
        variable.(field) = [variable.(field); variable.(avg_field)];

        newfield = strcat('test',num2str(test_case),'_std');
        std_field = strcat('test',num2str(test_case),'_',num2str(angle),'_std');
        variable.(newfield) = [variable.(newfield); variable.(std_field)];
    
    end

end 

color = "#0093AC";
color2 = "#91B5BB";%"#189AB4"; %"#0000FF";%1/255*[231,188,188];

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);
sz = 10;
lw = 2;
flipBool = 0;

x = [45 60 75 90 105 120 135 150 165 180];
y = variable.test1_avg;
disp(y)
SEM = variable.test1_std;
disp(SEM)
if flipBool
    p = plot(x, flip(y), 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color); hold on;
    xi = [x(1):1:x(end)];
    vid=interp1(x,y,xi,'spline');
    p2 = plot(xi,flip(vid), ':'); hold on;
    xticklabels({'180','165','150', '135', '120', '105', '90', '75', '60', '45'})
else
    p = plot(x, y, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color); hold on;
    xi = [x(1):1:x(end)];
    vid=interp1(x,y,xi,'spline');
    p2 = plot(xi,vid, ':'); hold on;
    
end
e = errorbar(x,y,SEM,"o"); hold on;
e.Color = color;
e.LineWidth = 1;

p2.LineWidth = lw;
p2.Color = color;
xlim([40,180])

j = 1;
x2 = x-j;
y = variable.test3_avg;
SEM = variable.test3_std;
if flipBool
    p = plot(x2, flip(y), 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2); hold on;
    vid2=interp1(x2+2*j,y,xi,'spline');
    p3 = plot(xi,flip(vid2), ':'); hold on;
else
    p = plot(x2, y, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color2, 'MarkerFaceColor', color2); hold on;
    vid2=interp1(x2,y,xi,'spline');
    p3 = plot(xi,vid2, ':'); hold on;
end
p3.LineWidth = lw;
p3.Color = color2;
%errorbar(x2,y,SEM,'b');
ylim([0 70]);
xlabel('target angles (deg)')
ylabel('Mean angle error (deg)')
%ylabel('angle mean absolute error (deg)')
ax.XTick = 45:15:180;
ax.FontSize = 18;
leg = legend('Haptic','','', 'No Haptic', '', '');
set(leg, 'edgeColor','w');


% figure;
% y = variable.test2_avg;
% SEM = variable.test2_std;
% scatter(x,y); hold on;
% errorbar(x,y,SEM);
% x2 = x-1;
% y = variable.test4_avg;
% SEM = variable.test4_std;
% scatter(x2,y,'filled'); hold on;
% errorbar(x2,y,SEM,'b');
% ylim([0 2.5]);
% xlabel('target angles (deg)')
% ylabel('angle mean absolute error (deg)')
% legend('H, V','','NH, V','');

%  %% Section 3 Forces vs. Angles
% 
% % create vectors to store force for each test case each target angle
% % create variables to store average of force for each test case each
% % target angle
% for test_case = 1:4
%     for angle = 45:15:180
%         my_field = strcat('test',num2str(test_case),'_',num2str(angle),'_force');
%         variable.(my_field) = [];
%         my_field = strcat('test',num2str(test_case),'_',num2str(angle),'_force_avg');
%         variable.(my_field) = 0;
%         my_field = strcat('test',num2str(test_case),'_',num2str(angle),'_force_std');
%         variable.(my_field) = 0;
%     end
% end
% 
% % populate those vectors with the force values
% for i = 1:size(M_new,1) % loop through all rows of M
%     
%     for test_case = 1:4 % loop through test cases 1-4
% 
%         for angle = 45:15:180 % loop through all ten target angles
% 
%             if M_new(i,5) == test_case && M_new(i,2) == angle % if you are at the right test case (1-4) and target angle row
%                 
%                 selectVal = M_new(i,9); % select the force value of that row
%                 my_field = strcat('test',num2str(test_case),'_',num2str(angle),'_force');
%                 variable.(my_field) = [variable.(my_field);selectVal]
%                 avg_field = strcat('test',num2str(test_case),'_',num2str(angle),'_force_avg');
%                 variable.(avg_field) = mean(variable.(my_field));
%                 std_field = strcat('test',num2str(test_case),'_',num2str(angle),'_force_std');
%                 variable.(std_field) = std(variable.(my_field));
%             end
% 
%         end
%     end
% 
% end
% 
% % create vectors to store test{test_case}_{angle}_force_avg values for each test
% variable.test1_force_avg = []; variable.test2_force_avg = []; variable.test3_force_avg = []; variable.test4_force_avg = [];
% variable.test1_force_std = []; variable.test2_force_std = []; variable.test3_force_std = []; variable.test4_force_std = [];
% 
% % populate those vectors with the average or std error for each target
% % angle
% for test_case = 1:4
% 
%     for angle = 45:15:180
%         
%         field = strcat('test',num2str(test_case),'_force_avg');
%         avg_field = strcat('test',num2str(test_case),'_',num2str(angle),'_force_avg');
%         variable.(field) = [variable.(field); variable.(avg_field)];
% 
%         newfield = strcat('test',num2str(test_case),'_force_std');
%         std_field = strcat('test',num2str(test_case),'_',num2str(angle),'_force_std');
%         variable.(newfield) = [variable.(newfield); variable.(std_field)];
%     
%     end
% 
% end 
% 
% % figure;
% % x = [45 60 75 90 105 120 135 150 165 180];
% % y = variable.test1_force_avg;
% % SEM = variable.test1_force_std;
% % scatter(x,y); hold on;
% % errorbar(x,y,SEM); hold on;
% % x2 = x-1;
% % y = variable.test3_force_avg;
% % SEM = variable.test3_force_std;
% % scatter(x2,y,'filled'); hold on;
% % errorbar(x2,y,SEM,'b');
% % % ylim([0 70]);
% % xlabel('target angles (deg)')
% % ylabel('force measured (N)')
% % legend('H, NV','','NH, NV','');
% 
% % figure;
% % y = variable.test2_force_avg;
% % SEM = variable.test2_force_std;
% % scatter(x,y); hold on;
% % errorbar(x,y,SEM);
% % x2 = x-1;
% % y = variable.test4_force_avg;
% % SEM = variable.test4_force_std;
% % scatter(x2,y,'filled'); hold on;
% % errorbar(x2,y,SEM,'b');
% % % ylim([0 2.5]);
% % xlabel('target angles (deg)')
% % ylabel('force measured (N)')
% % legend('H, V','','NH, V','');
% 
% 
% %%
% 
% % breakyaxes splits data in an axes so that data is in a low and high pane.
% %
% %   breakYAxes(splitYLim) splitYLim is a 2 element vector containing a range
% %   of y values from splitYLim(1) to splitYLim(2) to remove from the axes.
% %   They must be within the current yLimis of the axes.
% %
% %   breakYAxes(splitYLim,splitHeight) splitHeight is the distance to 
% %   seperate the low and high side.  Units are the same as 
% %   get(AX,'uints') default is 0.015
% % 
% %   breakYAxes(splitYLim,splitHeight,xOverhang) xOverhang stretches the 
% %   axis split graphic to extend past the top and bottom of the plot by
% %   the distance set by XOverhang.  Units are the same as get(AX,'units')
% %   default value is 0.015
% %
% %   breakYAxes(AX, ...) performs the operation on the axis specified by AX
% %
% function breakInfo = breakyaxis(varargin)
% 
%     %Validate Arguements
%     if nargin < 1 || nargin > 4
%        error('Wrong number of arguements'); 
%     end
% 
%     if isscalar(varargin{1}) && ishandle(varargin{1})
%         mainAxes = varargin{1};
%         argOffset = 1;
%         argCnt = nargin - 1;
%         if ~strcmp(get(mainAxes,'Type'),'axes')
%            error('Handle object must be Type Axes'); 
%         end
%     else
%         mainAxes = gca;
%         argOffset = 0;
%         argCnt = nargin;
%     end
%     
%     if (strcmp(get(mainAxes,'XScale'),'log'))
%         error('Log X Axes are not supported'); 
%     end
%     
%     if (argCnt < 3)
%         xOverhang = 0.015;
%     else
%         xOverhang = varargin{3 + argOffset};
%         if  numel(xOverhang) ~= 1 || ~isreal(xOverhang) || ~isnumeric(xOverhang)
%             error('XOverhang must be a scalar number');
%         elseif (xOverhang < 0)
%             error('XOverhang must not be negative');
%         end
%         xOverhang = double(xOverhang);
%     end
%     
%     if (argCnt < 2)
%         splitHeight = 0.015;
%     else
%         splitHeight = varargin{2 + argOffset};
%         if  numel(xOverhang) ~= 1 || ~isreal(xOverhang) || ~isnumeric(xOverhang)
%             error('splitHeight must be a scalar number');
%         elseif (xOverhang < 0)
%             error('splitHeight must not be negative');
%         end
%         splitHeight = double(splitHeight);
%     end
%     
%     splitYLim = varargin{1 + argOffset};
%     if numel(splitYLim) ~= 2 || ~isnumeric(splitYLim) || ~isreal(xOverhang)
%        error(splitYLim,'Must be a vector length 2');
%     end
%     splitYLim = double(splitYLim);
%     
%     mainYLim = get(mainAxes,'YLim');
%     if (any(splitYLim >= mainYLim(2)) || any(splitYLim <= mainYLim(1)))
%        error('splitYLim must be in the range given by get(AX,''YLim'')');
%     end
%     
%     mainPosition = get(mainAxes,'Position');
%     if (splitHeight > mainPosition(3) ) 
%        error('Split width is too large') 
%     end
%    
%     %We need to create 4 axes
%     % lowAxes - is used for the low y axis and low pane data
%     % highAxes - is used to the high y axis and high pane data
%     % annotationAxes - is used to display the x axis and title
%     % breakAxes - this is an axes with the same size and position as main
%     %   is it used to draw a seperator between the low and high side
%     
% 
%     %Grab Some Parameters from the main axis (e.g the one we are spliting)
%     mainYLim = get(mainAxes,'YLim');
%     mainXLim = get(mainAxes,'XLim');
%     mainPosition = get(mainAxes,'Position');
%     mainParent = get(mainAxes,'Parent');
%     mainHeight = mainPosition(4); %Positions have the format [low bottom width height]
%     %mainYRange = mainYLim(2) - mainYLim(1);
%     mainFigure = get(mainAxes,'Parent');
%     mainXColor = get(mainAxes,'XColor');
%     mainLineWidth = get(mainAxes,'LineWidth');
%     figureColor = get(mainFigure,'Color');
%     mainXTickLabelMode = get(mainAxes,'XTickLabelMode');
%     mainYLabel = get(mainAxes,'YLabel');
%     mainYDir = get(mainAxes,'YDir');
%     mainLayer = get(mainAxes,'Layer');
%     
%     %Save Main Axis Z Order
%     figureChildren = get(mainFigure,'Children');
%     zOrder = find(figureChildren == mainAxes);
%     
%     %Calculate where axesLow and axesHigh will be layed on screen
%     %And their respctive YLimits
%     lowYLimTemp = [mainYLim(1) splitYLim(1)];
%     highYLimTemp = [splitYLim(2) mainYLim(2)];
% 
%     lowYRangeTemp = lowYLimTemp(2) - lowYLimTemp(1);
%     highYRangeTemp = highYLimTemp(2) - highYLimTemp(1);
% 
%     lowHeightTemp = lowYRangeTemp / (lowYRangeTemp + highYRangeTemp) * (mainHeight - splitHeight);
%     highHeightTemp = highYRangeTemp / (lowYRangeTemp + highYRangeTemp) * (mainHeight - splitHeight);
% 
%     lowStretch = (lowHeightTemp + splitHeight/2) / lowHeightTemp;
%     lowYRange = lowYRangeTemp * lowStretch;
%     lowHeight = lowHeightTemp * lowStretch;
% 
%     highStretch = (highHeightTemp + splitHeight/2) / highHeightTemp;
%     highYRange = highYRangeTemp * highStretch;
%     highHeight = highHeightTemp * highStretch;
%     
%     lowYLim = [mainYLim(1) mainYLim(1)+lowYRange];
%     highYLim = [mainYLim(2)-highYRange mainYLim(2)];
%     
%     if (strcmp(mainYDir, 'normal')) 
%         lowPosition = mainPosition;
%         lowPosition(4) = lowHeight; 
% 
%         highPosition = mainPosition;    %(!!!) look here for position indices!
%         highPosition(2) = mainPosition(2) + lowHeight;
%         highPosition(4) = highHeight;
%     else
%         %Low Axis will actually go on the high side a vise versa
%         highPosition = mainPosition;
%         highPosition(4) = highHeight; 
% 
%         lowPosition = mainPosition;
%         lowPosition(2) = mainPosition(2) + highHeight;
%         lowPosition(4) = lowHeight;
%     end
%  
%     %Create the Annotations layer, if the Layer is top, draw the axes on
%     %top (e.g. after) drawing the low and high pane
%     if strcmp(mainLayer,'bottom')
%         annotationAxes = CreateAnnotaionAxes(mainAxes,mainParent)
%     end
%     
%     %Create and position the lowAxes. Remove all X Axis Annotations, the 
%     %title, and a potentially offensive tick mark 
%     lowAxes = copyobj(mainAxes,mainParent);
%     set(lowAxes,'Position', lowPosition, ...
%         'YLim', lowYLim, ... 
%         'XLim', mainXLim, ...
%         'XGrid' ,'off', ...
%         'XMinorGrid', 'off', ...
%         'XMinorTick','off', ...
%         'XTick', [], ...
%         'XTickLabel', [], ...
%         'box','off');
%     if strcmp(mainLayer,'bottom')
%         set(lowAxes,'Color','none');
%     end
%     delete(get(lowAxes,'XLabel')); 
%     delete(get(lowAxes,'YLabel'));
%     delete(get(lowAxes,'Title'));
%     
%     if strcmp(mainXTickLabelMode,'auto')
%         yTick =  get(lowAxes,'YTick');
%         set(lowAxes,'YTick',yTick(1:(end-1)));
%     end
%     
%     %Create and position the highAxes. Remove all X Axis annotations, the 
%     %title, and a potentially offensive tick mark 
%     highAxes = copyobj(mainAxes,mainParent);
%     set(highAxes,'Position', highPosition, ...
%         'YLim', highYLim, ...
%         'XLim', mainXLim, ...
%         'XGrid' ,'off', ...
%         'XMinorGrid', 'off', ...
%         'XMinorTick','off', ...
%         'XTick', [], ...
%         'XTickLabel', [], ...
%         'box','off');
%     if strcmp(mainLayer,'bottom') %(!!!) is it only about layers?
%         set(highAxes,'Color','none');
%     end
%     delete(get(highAxes,'XLabel')); 
%     delete(get(highAxes,'YLabel'));
%     delete(get(highAxes,'Title'));
%     
%     if strcmp(mainXTickLabelMode,'auto')
%         yTick =  get(highAxes,'YTick');
%         set(highAxes,'YTick',yTick(2:end));
%     end
% 
%         %Create the Annotations layer, if the Layer is top, draw the axes on
%     %top (e.g. after) drawing the low and high pane
%     if strcmp(mainLayer,'top')
%         annotationAxes = CreateAnnotaionAxes(mainAxes,mainParent);
%         set(annotationAxes, 'Color','none');
%     end
%     
%     %Create breakAxes, remove all graphics objects and hide all annotations
%     breakAxes = copyobj(mainAxes,mainParent);
%     children = get(breakAxes,'Children');
%     for i = 1:numel(children)
%        delete(children(i)); 
%     end
%     
%     set(breakAxes,'Color','none');
%     %Stretch the breakAxes horizontally to cover the vertical axes lines
%     orignalUnits = get(breakAxes,'Units');
%     set(breakAxes,'Units','Pixel');
%     breakPosition = get(breakAxes,'Position');
%     nudgeFactor = get(breakAxes,'LineWidth');
%     breakPosition(3) = breakPosition(3) +  nudgeFactor;
%     set(breakAxes,'Position',breakPosition);
%     set(breakAxes,'Units',orignalUnits);
% 
%     %Stretch the breakAxes horizontally to create an overhang for sylistic
%     %effect
%     breakPosition = get(breakAxes,'Position');
%     breakPosition(1) = breakPosition(1) - xOverhang;
%     breakPosition(3) = breakPosition(3) +  2*xOverhang;
%     set(breakAxes,'Position',breakPosition);
%     
%     %Create a sine shaped patch to seperate the 2 sides
%     breakYLim = [mainPosition(2) mainPosition(2)+mainPosition(4)];
%     set(breakAxes,'ylim',breakYLim);
%     theta = linspace(0,2*pi,100);
%     xPoints = linspace(mainXLim(1),mainXLim(2),100);
%     amp = splitHeight/2 * 0.9;
%     yPoints1 = amp * sin(theta) + mainPosition(2) + lowHeightTemp;
%     yPoints2 = amp * sin(theta) + mainPosition(2) + mainPosition(4) - highHeightTemp;
%     patchPointsY = [yPoints1 yPoints2(end:-1:1) yPoints1(1)];
%     patchPointsX = [xPoints  xPoints(end:-1:1)  xPoints(1)];
%     patch(patchPointsX,patchPointsY ,figureColor,'EdgeColor',figureColor,'Parent',breakAxes); %use of pathc(!!!)?
% 
%     %Create A Line To Delineate the low and high edge of the patch
%     line('yData',yPoints1,'xdata',xPoints,'Parent',breakAxes,'Color',mainXColor,'LineWidth',mainLineWidth);
%     line('yData',yPoints2,'xdata',xPoints,'Parent',breakAxes,'Color',mainXColor,'LineWidth',mainLineWidth);
% 
%     set(breakAxes,'Visible','off');
%     
%     %Make the old main axes invisiable
%     invisibleObjects = RecursiveSetVisibleOff(mainAxes);
% 
%     %Preserve the z-order of the figure
%     uistack([lowAxes highAxes breakAxes annotationAxes],'down',zOrder-1)
%     
%     %Set the rezise mode to position so that we can dynamically change the
%     %size of the figure without screwing things up
%     set([lowAxes highAxes breakAxes annotationAxes],'ActivePositionProperty','Position');
%  
%     %Playing with the titles labels etc can cause matlab to reposition
%     %the axes in some cases.  Mannually force the position to be correct. 
%     set([breakAxes annotationAxes],'Position',mainPosition);
%     
%     %Save the axes so we can unbreak the axis easily
%     breakInfo = struct();
%     breakInfo.lowAxes = lowAxes;
%     breakInfo.highAxes = highAxes;
%     breakInfo.breakAxes = breakAxes;
%     breakInfo.annotationAxes = annotationAxes;
%     breakInfo.invisibleObjects = invisibleObjects;
% end
% 
% function list = RecursiveSetVisibleOff(handle) 
%     list = [];
%     list = SetVisibleOff(handle,list);
%     
% end 
% 
% function list = SetVisibleOff(handle, list)
%     if (strcmp(get(handle,'Visible'),'on'))
%         set(handle,'Visible','off');
%         list = [list handle];
%     end
%     
%     children = get(handle,'Children');
%     for i = 1:numel(children)
%         list = SetVisibleOff(children(i),list);
%     end
% end
%     
% function annotationAxes = CreateAnnotaionAxes(mainAxes,mainParent)
% 
%     %Create Annotation Axis, Remove graphics objects, YAxis annotations
%     %(except YLabel) and make background transparent
%     annotationAxes = copyobj(mainAxes,mainParent);
%     
%     set(annotationAxes,'XLimMode','Manual');
%     
%     children = get(annotationAxes,'Children');
%     for i = 1:numel(children)
%        delete(children(i)); 
%     end
% 
%     %Save the yLabelpostion because it will move when we delete yAxis
%     %ticks
%     yLabel = get(annotationAxes,'YLabel');
%     yLabelPosition = get(yLabel,'Position');
%     
%     set(annotationAxes,'YGrid' ,'off', ...
%         'YMinorGrid', 'off', ...
%         'YMinorTick','off', ...
%         'YTick', [], ...
%         'YTickLabel', []);
%     
%     %Restore the pevious label postition
%     set(yLabel,'Position',yLabelPosition);
% end
% 
% %%
% function varargout=sigstar(groups,stats,nosort)
%     % sigstar - Add significance stars to bar charts, boxplots, line charts, etc,
%     %
%     % H = sigstar(groups,stats,nsort)
%     %
%     % Purpose
%     % Add stars and lines highlighting significant differences between pairs of groups. 
%     % The user specifies the groups and associated p-values. The function handles much of 
%     % the placement and drawing of the highlighting. Stars are drawn according to:
%     %   * represents p<=0.05
%     %  ** represents p<=1E-2
%     % *** represents p<=1E-3
%     %
%     %
%     % Inputs
%     % groups - a cell array defining the pairs of groups to compare. Groups defined 
%     %          either as pairs of scalars indicating locations along the X axis or as 
%     %          strings corresponding to X-tick labels. Groups can be a mixture of both 
%     %          definition types.
%     % stats -  a vector of p-values the same length as groups. If empty or missing it's 
%     %          assumed to be a vector of 0.05s the same length as groups. Nans are treated
%     %          as indicating non-significance.
%     % nsort -  optional, 0 by default. If 1, then significance markers are plotted in 
%     %          the order found in groups. If 0, then they're sorted by the length of the 
%     %          bar.
%     %
%     % Outputs
%     % H - optionally return handles for significance highlights. Each row is a different
%     %     highlight bar. The first column is the line. The second column is the text (stars).
%     %     
%     %
%     % Examples
%     % 1. 
%     % bar([5,2,1.5])
%     % sigstar({[1,2], [1,3]})
%     %
%     % 2. 
%     % bar([5,2,1.5])
%     % sigstar({[2,3],[1,2], [1,3]},[nan,0.05,0.05])
%     %
%     % 3.  **DOESN'T WORK IN 2014b**
%     % R=randn(30,2);
%     % R(:,1)=R(:,1)+3;
%     % boxplot(R)
%     % set(gca,'XTick',1:2,'XTickLabel',{'A','B'})
%     % H=sigstar({{'A','B'}},0.01);
%     % ylim([-3,6.5])
%     % set(H,'color','r')
%     %
%     % 4. Note the difference in the order with which we define the groups in the 
%     %    following two cases. 
%     % x=[1,2,3,2,1];
%     % subplot(1,2,1)
%     % bar(x)
%     % sigstar({[1,2], [2,3], [4,5]})
%     % subplot(1,2,2)
%     % bar(x)
%     % sigstar({[2,3],[1,2], [4,5]})
%     %
%     % ALSO SEE: demo_sigstar
%     %
%     % KNOWN ISSUES:
%     % 1. Algorithm for identifying whether significance bar will overlap with 
%     %    existing plot elements may not work in some cases (see line 277)
%     % 2. Bars may not look good on exported graphics with small page sizes.
%     %    Simply increasing the width and height of the graph with the 
%     %    PaperPosition property of the current figure should fix things.
%     %
%     % Rob Campbell - CSHL 2013
% 
% 
% 
%     %Input argument error checking
% 
%     %If the user entered just one group pair and forgot to wrap it in a cell array 
%     %then we'll go easy on them and wrap it here rather then generate an error
%     if ~iscell(groups) & length(groups)==2
%         groups={groups};
%     end
% 
%     if nargin<2 
%         stats=repmat(0.05,1,length(groups));
%     end
%     if isempty(stats)
%         stats=repmat(0.05,1,length(groups));
%     end
%     if nargin<3
%         nosort=0;
%     end
% 
% 
% 
% 
%     %Check the inputs are of the right sort
%     if ~iscell(groups)
%         error('groups must be a cell array')
%     end
% 
%     if ~isvector(stats)
%         error('stats must be a vector')
%     end
% 
%     if length(stats)~=length(groups)
%         error('groups and stats must be the same length')
%     end
% 
% 
% 
% 
% 
% 
%     %Each member of the cell array groups may be one of three things:
%     %1. A pair of indices.
%     %2. A pair of strings (in cell array) referring to X-Tick labels
%     %3. A cell array containing one index and one string
%     %
%     % For our function to run, we will need to convert all of these into pairs of
%     % indices. Here we loop through groups and do this. 
% 
%     xlocs=nan(length(groups),2); %matrix that will store the indices 
%     xtl=get(gca,'XTickLabel');  
% 
%     for ii=1:length(groups)
%         grp=groups{ii};
% 
%         if isnumeric(grp)
%             xlocs(ii,:)=grp; %Just store the indices if they're the right format already
% 
%         elseif iscell(grp) %Handle string pairs or string/index pairs
% 
%             if isstr(grp{1})
%                 a=strmatch(grp{1},xtl);
%             elseif isnumeric(grp{1})
%                 a=grp{1};
%             end
%             if isstr(grp{2})
%                 b=strmatch(grp{2},xtl);
%             elseif isnumeric(grp{2})
%                 b=grp{2};
%             end
% 
%             xlocs(ii,:)=[a,b];
%         end
% 
%         %Ensure that the first column is always smaller number than the second
%         xlocs(ii,:)=sort(xlocs(ii,:));
% 
%     end
% 
%     %If there are any NaNs we have messed up. 
%     if any(isnan(xlocs(:)))
%         error('Some groups were not found')
%     end
% 
% 
% 
% 
% 
% 
%     %Optionally sort sig bars from shortest to longest so we plot the shorter ones first
%     %in the loop below. Usually this will result in the neatest plot. If we waned to 
%     %optimise the order the sig bars are plotted to produce the neatest plot, then this 
%     %is where we'd do it. Not really worth the effort, though, as few plots are complicated
%     %enough to need this and the user can define the order very easily at the command line. 
%     if ~nosort
%         [~,ind]=sort(xlocs(:,2)-xlocs(:,1),'ascend');
%         xlocs=xlocs(ind,:);groups=groups(ind);
%         stats=stats(ind);
%     end
% 
% 
% 
%     %-----------------------------------------------------
%     %Add the sig bar lines and asterisks 
%     holdstate=ishold;
%     hold on
% 
%     H=ones(length(groups),2); %The handles will be stored here
% 
%     y=ylim;
%     yd=myRange(y)*0.05; %separate sig bars vertically by 5% 
% 
%     for ii=1:length(groups)
%         thisY=findMinY(xlocs(ii,:))+yd;
%         H(ii,:)=makeSignificanceBar(xlocs(ii,:),thisY,stats(ii));
%     end
%     %-----------------------------------------------------
% 
% 
% 
% 
%     %Now we can add the little downward ticks on the ends of each line. We are
%     %being extra cautious and leaving this it to the end just in case the y limits
%     %of the graph have changed as we add the highlights. The ticks are set as a
%     %proportion of the y axis range and we want them all to be the same the same
%     %for all bars.
%     yd=myRange(ylim)*0.01; %Ticks are 1% of the y axis range
%     for ii=1:length(groups)
%         y=get(H(ii,1),'YData');
%         y(1)=y(1)-yd;
%         y(4)=y(4)-yd;   
%         set(H(ii,1),'YData',y)
%     end
% 
% 
% 
% 
%     %Be neat and return hold state to whatever it was before we started
%     if ~holdstate
%         hold off
%     elseif holdstate
%         hold on
%     end
% 
% 
%     %Optionally return the handles to the plotted significance bars (first column of H)
%     %and asterisks (second column of H).
%     if nargout>0
%         varargout{1}=H;
%     end
% 
% 
% end %close sigstar
% 
% 
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %Internal functions
% 
% function H=makeSignificanceBar(x,y,p)
%     %makeSignificanceBar produces the bar and defines how many asterisks we get for a 
%     %given p-value
% 
% 
%     if p<=1E-3
%         stars='***'; 
%     elseif p<=1E-2
%         stars='**';
%     elseif p<=0.05
%         stars='*';
%     elseif isnan(p)
%         stars='n.s.';
%     else
%         stars='';
%     end
%             
%     x=repmat(x,2,1);
%     y=repmat(y,4,1);
% 
%     H(1)=plot(x(:),y,'-k','LineWidth',1.5,'Tag','sigstar_bar');
% 
%     %Increase offset between line and text if we will print "n.s."
%     %instead of a star. 
%     if ~isnan(p)
%         offset=0.005;
%     else
%         offset=0.02;
%     end
% 
%     starY=mean(y)+myRange(ylim)*offset;
%     H(2)=text(mean(x(:)),starY,stars,...
%         'HorizontalAlignment','Center',...
%         'BackGroundColor','none',...
%         'Tag','sigstar_stars');
% 
%     Y=ylim;
%     if Y(2)<starY
%         ylim([Y(1),starY+myRange(Y)*0.05])
%     end
% 
% 
% end %close makeSignificanceBar
% 
% 
% 
% function Y=findMinY(x)
%     % The significance bar needs to be plotted a reasonable distance above all the data points
%     % found over a particular range of X values. So we need to find these data and calculat the 
%     % the minimum y value needed to clear all the plotted data present over this given range of 
%     % x values. 
%     %
%     % This version of the function is a fix from Evan Remington
%     oldXLim = get(gca,'XLim');
%     oldYLim = get(gca,'YLim');
% 
%     axis(gca,'tight')
%     
%     %increase range of x values by 0.1 to ensure correct y max is used
%     x(1)=x(1)-0.1;
%     x(2)=x(2)+0.1;
%     
%     set(gca,'xlim',x) %Matlab automatically re-tightens y-axis
% 
%     yLim = get(gca,'YLim'); %Now have max y value of all elements within range.
%     Y = max(yLim);
% 
%     axis(gca,'normal')
%     set(gca,'XLim',oldXLim,'YLim',oldYLim)
% 
% end %close findMinY
% 
% 
% function rng=myRange(x)
%     %replacement for stats toolbox range function
%     rng = max(x) - min(x);
% end %close myRange
% 
% 
% 
% 
% 
% 
% 
% 
