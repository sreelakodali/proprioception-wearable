file = '2024-04-03_20-40';
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/';
onePoke = readmatrix(strcat(path,file, '/processed_', file,'.csv'),'NumHeaderLines',1);

time = onePoke(:,1);
commandMM_1p = interp1([47, 139],[0, 20],onePoke(:,3));
measuredMM_1p = interp1([986, 28],[0, 20],onePoke(:,4));
force_1p = onePoke(:,5);
nTrials = onePoke(:,9);

freq = fft(force_1p);
Fs = 1/(177.477 - 177.325);
L = length(force_1p);

figure;
set(gcf,'color','white')
ax = gca(gcf);
plot(time, force_1p);

figure;
set(gcf,'color','white')
ax = gca(gcf);
plot(Fs/L*(0:L-1), abs(freq));

