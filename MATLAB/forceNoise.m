close all;
%file = '2024-07-03_20-45_60Hz';
%file = '2024-07-03_20-40_30Hz';
%file = '2024-07-03_20-28_12Hz';
file = '2024-07-01_17-04_6Hz';
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/additionalData/';
onePoke = readmatrix(strcat(path,file, '/raw_', file,'.csv'),'NumHeaderLines',1);

yMax = 500;
time = onePoke(:,1);
command = onePoke(:,3);
measured = onePoke(:,4);
%commandMM_1p = interp1([47, 139],[0, 20],onePoke(:,3));
%measuredMM_1p = interp1([986, 28],[0, 20],onePoke(:,4));
force_1p = onePoke(:,5);
%nTrials = onePoke(:,9);

diff = zeros(size(time, 1)-1, 1);
for i = 1:(size(onePoke,1)-1)
    d = time(i+1,1) - time(i,1);
    diff(i,1) = d;
    %disp(d);
end

Fs = 1000/mean(diff);

%hpFilt = designfilter('highpassfir', 'Stop')
%HPF = dsp.HighpassFilter('FIR');

%filtered = medfilt1(force_1p);
filtered6 = medfilt1(force_1p,10);

f_filter = 0.1; % 1 Hz

filtered2 = lowpass(force_1p, f_filter*2/Fs);
filtered3 = round(filtered2);
w = 5;
coeffWindow = ones(1,w)/w;
filtered4 = filter(coeffWindow, 1, force_1p);
filtered5 = floor(filtered4);
filtered6 = medfilt1(force_1p,20);
filtered6 = floor(filtered6);
%filtered =  lowpass(force_1p, 2*2/Fs);
%filtered3 = bandpass(force_1p, [.1, .167], Fs);
%filtered3 = highpass(force_1p, .167, Fs);

%filtered3 = 255 + filtered3;

fftY = fft(force_1p);
magY = abs(fftY);
magYshift = abs(fftshift(fftY));
L = length(force_1p);

%
figure;
set(gcf,'color','white')
ax = gca(gcf);
plot(time, force_1p, time, filtered2-2, time, filtered3-5, time, filtered4-7, time, filtered5-9, time, filtered6-11);
ylim([240,260]);
%ylim([245,258]);
title("Force vs time", 'FontSize',18)
ylabel("force (raw vhoalue)", 'FontSize',18)
xlabel("time (ms)", 'FontSize',18)

% figure;
% set(gcf,'color','white')
% freqz
% figure;
% set(gcf,'color','white')
% ax = gca(gcf);
% plot(Fs/L*(0:L-1), magY);
% ylim([0,yMax]);
% title("Complex Magnitude of Force FFT Spectrum", 'FontSize',18)
% ylabel("|fft(force)|", 'FontSize',18)
% xlabel("f (Hz)", 'FontSize',18)
% 
% figure;
% set(gcf,'color','white')
% ax = gca(gcf);
% plot(Fs/L*(-L/2:L/2-1), magYshift);
% ylim([0,yMax]);
% title("Force fft Spectrum in the Positive and Negative Frequencies", 'FontSize',18)
% ylabel("|fft(force)|", 'FontSize',18)
% xlabel("f (Hz)", 'FontSize',18)


P2 = abs(fftY/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

% figure;
% set(gcf,'color','white')
% ax = gca(gcf);
% plot(Fs/L*(0:(L/2)),P1,"LineWidth",3)
% ylim([0,0.5]);
% title("Single-Sided Amplitude Spectrum of X(t)", 'FontSize',18)
% xlabel("f (Hz)", 'FontSize',18)
% ylabel("|P1(f)|", 'FontSize',18)
