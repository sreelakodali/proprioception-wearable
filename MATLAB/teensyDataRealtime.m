path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/additionalData/';

file = '2024-08-29_22-29';
data = readmatrix(strcat(path,file, '/raw_', file,'.csv'),'NumHeaderLines',0);
time = data(:,1)/1000;
rawCommand = data(:,2);
command = interp1([-1, 4098],[0, 27],rawCommand);
rawMeasured = data(:,3);
measured = interp1([0, 4098],[0, 27],data(:,3));
force = data(:,4);
filteredForce = data(:,5);
filteredForce1 = data(:,6);

figure;
set(gcf,'color','white')
gca(gcf);
plot(time, command);
yyaxis right;
plot(time,force, LineStyle="-"); hold on;
plot(time,filteredForce, LineStyle="-", Color='blue'); hold on;
plot(time,filteredForce1, LineStyle="-", Color='green'); hold on;
ylim([245,280]);