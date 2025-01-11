file = 'subjectsk_2025-01-11_03-31';
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/';
data = readmatrix(strcat(path,file, '/raw_device1_', file,'.csv'),'NumHeaderLines',0);


data = data(600:end, :);
time = data(:,1)/1000;
setpoints = data(:,2);
force = data(:,3);

figure;
set(gcf,'color','white');
gca(gcf);
plot(time, setpoints); hold on;
plot(time, force);