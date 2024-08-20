function [command, measured] = plotFreqSpectrum(file, str, fileType, varargin)

%close all;
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/additionalData/';

if fileType == "readSerial"
    data = readmatrix(strcat(path,file, '/raw_', file,'.csv'),'NumHeaderLines',0);
    time = data(:,1)/1000;
    rawCommand = data(:,2);
    command = interp1([47, 139],[0, 20],rawCommand);
    rawMeasured = data(:,3);
    measured = interp1([986, 28],[0, 20],data(:,3));
    force = data(:,4);
elseif fileType == "staircasing"
    path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/JND_Data/';
    data = readmatrix(strcat(path,file, '/raw_', file,'.csv'),'NumHeaderLines',0);
    time = data(:,1)/1000;
    rawCommand = data(:,3);
    command = interp1([47, 139],[0, 20],rawCommand);
    rawMeasured = data(:,4);
    measured = interp1([986, 28],[0, 20],data(:,3));
    force = data(:,5);
end

force = (force - min(force)) * 45/512;
tdiff = diff(time);
Fs = 1/mean(tdiff);

%disp(str);
if str == "rawC"
    %disp("here");
    signal = rawCommand;
elseif str == "command"
    %disp("here2");
    signal = command;
elseif str == "rawM"
    %disp("here3");
    signal = rawMeasured;
elseif str == "measured"
    %disp("here4");
    signal = measured;
elseif str == "force"
    %disp("here5");
    signal = force;
else
    %disp("here6");
    signal = force;
end

fftY = fft(signal);
L = length(signal);

% Plot signal in time domain
figure;
set(gcf,'color','white')
gca(gcf);
scatter(measured,signal);
P = polyfit(measured,signal,1);
yfit = polyval(P,measured);
hold on;
plot(measured,yfit,'r-.');
eqn = string(" Linear: y = " + P(1)) + "x + " + string(P(2));
text(min(measured),max(signal),eqn,"HorizontalAlignment","left","VerticalAlignment","top")
title(strcat(str, " vs. displacement"), 'FontSize',18);
xlabel("displacement (mm)", 'FontSize',18)
ylabel(str, 'FontSize',18)

magY = abs(fftY);
magYshift = abs(fftshift(fftY));

P2 = abs(fftY/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
yMax = 10;
yLimitOn = 0;

if (~isempty(varargin))
    yMax = varargin{1};
    yLimitOn = 1;
end

%frequency spectrum 
figure;
set(gcf,'color','white')
gca(gcf);
plot(Fs/L*(0:(L/2)),P1,"LineWidth",3)
if (yLimitOn)
    ylim([0,yMax]);
end
title(strcat("Single-Sided Amplitude Spectrum of ", str, "(t)"), 'FontSize',18);
xlabel("f (Hz)", 'FontSize',18)
ylabel("|P1(f)|", 'FontSize',18)

% figure;
% set(gcf,'color','white')
% freqz
% figure;
% set(gcf,'color','white')
% ax = gca(gcf);
% plot(Fs/L*(0:L-1), magY);
% % ylim([0,yMax]);
% title("Complex Magnitude of Force FFT Spectrum", 'FontSize',18)
% ylabel("|fft(signal)|", 'FontSize',18)
% xlabel("f (Hz)", 'FontSize',18)
% 
% figure;
% set(gcf,'color','white')
% ax = gca(gcf);
% plot(Fs/L*(-L/2:L/2-1), magYshift);
% % ylim([0,yMax]);
% title("Force fft Spectrum in the Positive and Negative Frequencies", 'FontSize',18)
% ylabel("|fft(signal)|", 'FontSize',18)
% xlabel("f (Hz)", 'FontSize',18)


end