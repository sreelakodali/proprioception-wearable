file = 'subjectsk_2025-01-04_02-00';
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/';
data = readmatrix(strcat(path,file, '/NEW_processed_device1_', file,'.csv'),'NumHeaderLines',0);


x = data(:,1) * (27.0 / 4095);
fo = data(:,2);

%fitobj = polyfit(x,fo, 1);

x1 = 0:0.1:20;
y1 = polyval(fitobj, x1);
figure;
set(gcf,'color','white');
gca(gcf);
scatter(x(67:295),fo(67:295)); hold on;
%plot(x1, y1); hold on;
%plot(x(67:295), gradient(x(67:295), fo(67:295)));
% 
% SStot = sum((fo-mean(fo)).^2);                    % Total Sum-Of-Squares
% SSres = sum((y-yfit).^2);                       % Residual Sum-Of-Squares
% Rsq = 1-SSres/SStot;  