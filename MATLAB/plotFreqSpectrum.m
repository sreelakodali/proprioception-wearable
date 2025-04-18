function [time, force] = plotFreqSpectrum(file, str, fileType, varargin)

%close all;
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/';

if fileType == "readSerial"
    data = readmatrix(strcat(path,file, '/raw_', file,'.csv'),'NumHeaderLines',0);
%     data2 = readmatrix(strcat(path,'2024-08-29_18-54', '/raw_', '2024-08-29_18-54','.csv'),'NumHeaderLines',0);
%     data3 = readmatrix(strcat(path,'2024-08-29_20-38', '/raw_', '2024-08-29_20-38','.csv'),'NumHeaderLines',0);
%     data4 = readmatrix(strcat(path,'2024-08-29_21-21', '/raw_', '2024-08-29_21-21','.csv'),'NumHeaderLines',0);
%     %raw = data2(:,1);
%     filteredTeensy = data2(:,2);
%     filteredTeensyFloat = data3(:,2);
%     filteredTeensy16 = data3(:,3);
% 
%     filteredTeesnyAll = data4(:,2);
%     filteredTeensy1by1 = data4(:,3);
% 
%     l1 = length(filteredTeensy);

    time = data(:,1)/1000;
%     rawCommand = data(:,2);
%     command = interp1([0, 4098],[0, 27],rawCommand);
%     rawMeasured = data(:,3);
%     measured = interp1([0, 4098],[0, 27],data(:,3));
    force = data(:,2);
    filteredForce1 = data(:,3);
    filteredForce2 = data(:,4);
    l1 = length(time);
    %filteredForce3 = data(:,7);

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

force = (force - min(force));
filteredForce1 = (filteredForce1 - min(filteredForce1));
filteredForce2 = (filteredForce2 - min(filteredForce2));
%filteredForce3 = (filteredForce3 - min(filteredForce3)) + 5;
% filteredForce4 = filteredTeensy + 20;
% filteredForce5 = filteredTeensyFloat + 25;
% filteredForce6 = filteredTeensy16 + 10;
% filteredForce7 = filteredTeesnyAll + 10;
% filteredForce8 = filteredTeensy1by1 + 15;

time = time(1:l1);
tdiff = diff(time);
Fs = 1/mean(tdiff);
disp(Fs);

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
plot(time,force, time,filteredForce1, time,filteredForce2);
%plot(time,force(1:l1), time,filteredForce2(1:l1), time,filteredForce3(1:l1), time,filteredForce6);

% disp(size(force,1)-20);
% for i = 1:20:(size(force,1)-20)
%     str = sprintf('%d, %d, %d, %d, %d, %d, %d, %d, %d, %d,', force(i), force(i+1), force(i+2), force(i+3), force(i+4), force(i+5), force(i+6), force(i+7), force(i+8), force(i+9));
%     i = i + 10;
%     str2 = sprintf(' %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, ', force(i), force(i+1), force(i+2), force(i+3), force(i+4), force(i+5), force(i+6), force(i+7), force(i+8), force(i+9));
%     disp(strcat(str,str2));
% end

% scatter(measured,signal);
% P = polyfit(measured,signal,1);
% yfit = polyval(P,measured);
% hold on;
% plot(measured,yfit,'r-.');
% eqn = string(" Linear: y = " + P(1)) + "x + " + string(P(2));
% text(min(measured),max(signal),eqn,"HorizontalAlignment","left","VerticalAlignment","top")
% title(strcat(str, " vs. displacement"), 'FontSize',18);
% xlabel("displacement (mm)", 'FontSize',18)
% ylabel(str, 'FontSize',18)
% 
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
% if (yLimitOn)
%     ylim([0,yMax]);
% end
ylim([0,2]);
title(strcat("Single-Sided Amplitude Spectrum of ", str, "(t)"), 'FontSize',18);
xlabel("f (Hz)", 'FontSize',18)
ylabel("|P1(f)|", 'FontSize',18)

figure;
set(gcf,'color','white')
ax = gca(gcf);
plot(Fs/L*(0:L-1), magY);
% ylim([0,yMax]);
title("Complex Magnitude of Force FFT Spectrum", 'FontSize',18)
ylabel("|fft(signal)|", 'FontSize',18)
xlabel("f (Hz)", 'FontSize',18)

figure;
set(gcf,'color','white')
ax = gca(gcf);
plot(Fs/L*(-L/2:L/2-1), magYshift);
% ylim([0,yMax]);
title("Force fft Spectrum in the Positive and Negative Frequencies", 'FontSize',18)
ylabel("|fft(signal)|", 'FontSize',18)
xlabel("f (Hz)", 'FontSize',18)


end