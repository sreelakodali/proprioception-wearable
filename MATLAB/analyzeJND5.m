%close all
%clear
color="#0C1446";%reversal
color2 = "#29A0B1";%staircase
color3 = "#FF9636"; %JND
color4 = "#190204"; %reference
color5 = "#4B8378";
color6 = "#DF362D";
color7 = "#880ED4";


%onePoke = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/2024-01-30_20-47/processed_2024-01-30_20-47.csv','NumHeaderLines',1);
onePoke = readmatrix('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/2024-03-18_22-21/processed_2024-03-18_22-21.csv','NumHeaderLines',1);



figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf); 

time = onePoke(:,1);
command = onePoke(:,3);
measured = onePoke(:,4);
force = onePoke(:,5);

commandMM = interp1([47, 139],[0, 20],command);
measuredMM = interp1([986, 30],[0, 20],measured);

plot(time,commandMM); hold on;
plot(time,measuredMM); hold on;

yyaxis right

plot(time,force); hold on;
