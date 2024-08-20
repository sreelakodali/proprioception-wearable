%clear;
close all;

file = '2024-07-16_20-35'; % without rigid
file2 = '2024-07-16_20-56'; % with rigid
% file = '2024-07-16_18-15'; % with rigid 
% file3 = '2024-07-16_19-00'; % with rigid second time
% file2= '2024-07-16_18-40'; % without rigid 
% file = '2024-07-15_19-51';
%file = '2024-07-10_19-13'; % with rigid band/bangle
%'2024-07-09_20-33-me120';
% 2024-07-09_20-33-me120
% 2024-07-09_20-17-cow
% 2024-07-09_20-25-me99
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/additionalData/';
data = readmatrix(strcat(path,file, '/raw_', file,'.csv'),'NumHeaderLines',0);

data2 = readmatrix(strcat(path,file2, '/raw_', file2,'.csv'),'NumHeaderLines',0);
time2 = data2(:,1)/1000;
force2 = data2(:,4);
command2 = interp1([47, 139],[0, 20],data2(:,2));
measured2 = interp1([986, 28],[0, 20],data2(:,3));
force2Ventral = data2(:,5);

% data3 = readmatrix(strcat(path,file3, '/raw_', file3,'.csv'),'NumHeaderLines',0);
% time3 = data3(:,1)/1000;
% force3 = data3(:,4);
% command3 = interp1([47, 139],[0, 20],data3(:,2));
% measured3 = interp1([986, 28],[0, 20],data3(:,3));


time = data(:,1)/1000;
rawCommand = data(:,2);
command = interp1([47, 139],[0, 20],data(:,2));
measured = interp1([986, 28],[0, 20],data(:,3));
forceVentral = data(:,5);

%commandMM_1p = interp1([47, 139],[0, 20],onePoke(:,3));
%measuredMM_1p = interp1([986, 28],[0, 20],onePoke(:,4));
force = data(:,4);
gradM = [diff(measured)];
gradM = [gradM; 0];
idx = find(abs(gradM) >= 0.165);
gradF = [diff(force)];
gradF = [gradF; 0];


tdiff = zeros(size(time, 1)-1, 1);
for i = 1:(size(data,1)-1)
    d = time(i+1,1) - time(i,1);
    tdiff(i,1) = d;
    %disp(d);
end
Fs = 1/mean(tdiff);
fftY = fft(force);
magY = abs(fftY);
magYshift = abs(fftshift(fftY));
L = length(force);
yMax= 10;

fftPos = fft(data(:,3));
magfftPos = abs(fftPos);
magfftPosShift = abs(fftshift(fftPos));
L_Pos = length(data(:,3));

P2_Pos = abs(fftPos/L_Pos);
P1_Pos = P2_Pos(1:L_Pos/2+1);
P1_Pos(2:end-1) = 2*P1_Pos(2:end-1);


P2 = abs(fftY/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

%frequency spectrum 
figure;
set(gcf,'color','white')
gca(gcf);
plot(Fs/L*(0:(L/2)),P1,"LineWidth",3)
ylim([0,yMax]);
title("Single-Sided Amplitude Spectrum of Force(t)", 'FontSize',18)
xlabel("f (Hz)", 'FontSize',18)
ylabel("|P1(f)|", 'FontSize',18)


%frequency spectrum actuator position
figure;
set(gcf,'color','white')
gca(gcf);
plot(Fs/L_Pos*(0:(L_Pos/2)),P1_Pos,"LineWidth",3)
%ylim([0,yMax]);
title("Single-Sided Amplitude Spectrum of Measured(t)", 'FontSize',18)
xlabel("f (Hz)", 'FontSize',18)
ylabel("|P1(f)|", 'FontSize',18)



%filter time
f_filter = 0.08; % unit is in Hz

[filteredLPF, d] = lowpass(force, f_filter*2/Fs);
filteredLPFr = round(filteredLPF);
w = 20;
coeffWindow = ones(1,w)/w;
filteredAVG = filter(coeffWindow, 1, force);
filteredAVGf = floor(filteredAVG);
filteredMedian = medfilt1(force,25);
filteredMedianf = floor(filteredMedian);
filteredHd = round(filter(Hd,force));
filteredHd2 = round(skFilter(force));

% [z,p,k] = butter(3,f_filter*2/Fs);
% [s, g]  = zp2sos(z,p,k);
% num = s(:,1:3);
% den = s(:,4:6);    
% sosFilter = dsp.SOSFilter(num,den,...
%     'HasScaleValues',true,...
%     ScaleValues=g);
% 
% filteredButter = sosFilter(force);
% fvtool(sosFilter,'Fs',Fs)

Fcutoff = 0.25;
[z,p,k] = butter(10,Fcutoff/(6.67/2));
[s, g]  = zp2sos(z,p,k);
num = s(:,1:3);
den = s(:,4:6);
    
sosFilter = dsp.SOSFilter(num,den,...
    'HasScaleValues',true,...
    'ScaleValues',g)
filteredButter = round(sosFilter(force));
% fvtool(d,'Fs',Fs)
% fvtool(sosFilter,'Fs',Fs)

gradForceLPFr = [diff(filteredLPF); 0];
idxLocalMax = islocalmax(gradForceLPFr, 'MinSeparation',50);
idxLocalMax2 = find(idxLocalMax);
idx4 = [];
for i = 1:(length(idxLocalMax2) - 1)
    idx4 = [idx4; floor((idxLocalMax2(i) + idxLocalMax2(i+1))/2) ];
end
%filteredMode = colfilt(f, [5 1], 'sliding', @mode); %modefilt(force, [w,1]);

% ------ we're going to try filtering certain portions of the signal

buffer = 20;
endBuffer = 80;
forceFilteredSegments = force;
idx2 = [];
filterBool = 0;
j = 0;
for i = 230:(length(force)-200) %230
    if (ismember(i, idx) &&  ~(ismember(i+1, idx)))
        idx2(end+1) = i;
%         filterBool = 1; % you're entering a window to filter
%         j = 0;

        j = i + buffer;
        v = floor(filter(coeffWindow, 1, force(j:i+endBuffer,1)));
        %v = floor(medfilt1(force(j:i+endBuffer,1),20)); % % %-1*ones(61,1);  
        idxLow = find(v<250);
        v(idxLow) = force(idxLow + j);
        forceFilteredSegments(j:i+endBuffer,1) = v;
    end
end

% figure;
% set(gcf,'color','white')
% ax = gca(gcf);
% scatter(rawCommand,measured, 'filled');



% for LPF, higher than 0.6 or 0.4 there's more noise. below that looks the same
% window of 50 for moving average
figure;
set(gcf,'color','white')
ax = gca(gcf);
%plot(time, command); hold on;
 plot(time, measured, LineStyle="-", Color='cyan'); hold on; % without rigid
 plot(time, gradForceLPFr); hold on;
% plot(time2, measured2, LineStyle="-", Color='green'); hold on % with rigid
% plot(time, gradM, LineStyle="-"); hold on; %
% plot(measured3(436:end,:)-measured3(436,1), force3(436:end,:), Color='cyan'); hold on % with rigid again
ylim([-1,20]);
% scatter(time(idx2), measured(idx2), 20, 'red', 'filled'); hold on;
% %plot(time, gradM); hold on;

newCmds = rawCommand(idx2);
%plot(time, gradF); hold on;
yyaxis right;
%plot(time, force); hold on;
%plot(time, forceFilteredSegments-10, 'Color','black', 'LineStyle','-');
plot(time, force, LineStyle="-", Color='red'); hold on; % without rigid
%plot(time, forceVentral, LineStyle="-", Color='black'); hold on % without rigid
%plot(time2, force2, LineStyle="-", Color='magenta'); hold on % with rigid
%plot(time2, force2Ventral, LineStyle="-", Color='blue'); hold on % with rigid
%scatter(time(idx2), force(idx2), 20, 'red', 'filled');
%plot(grad); hold on;
% plot(time, force, LineStyle="-", Color='red'); hold on;
% plot(time2, force2, LineStyle="-", Color='magenta'); hold on;
% plot(time3, force3, LineStyle="-", Color='green'); hold on;



plot(time, filteredLPFr+10, LineStyle="-", Color='blue'); hold on;
plot(time, filteredButter+15, LineStyle="-", Color='green'); hold on;
plot(time, filteredHd+20, LineStyle="-", Color='magenta'); hold on;
plot(time, filteredHd2+30, LineStyle="-", Color='blue', Marker='none'); hold on;


%scatter(time(idx4), filteredLPFr(idx4) + 10, 20, "black", 'filled'); hold on;   

%plot(time, filteredAVGf+10, LineStyle="-", Color='magenta'); hold on;
%plot(time, filteredMedianf+15, LineStyle="-", Color='green'); hold on;
% plot(time, medfilt1(filteredAVGf,20)+25, LineStyle="-", Color='cyan', Marker='none'); hold on;

ylim([240,370]);
% plot(time, round(lowpass(filteredAVGf, 0.1*2/Fs)) + 20); hold on;

%plot(time, round(filter(ones(1,20)/20, 1, filteredLPFr)) + 20); hold on;
%plot(time, round(filter(ones(1,20)/20, 1, filteredLPF)) + 25); hold on;

% plot(time, round(lowpass(filteredMedianf, 0.1*2/Fs)) + 25); hold on;
wArr = 20:10:100;
f_filterArr = 0.6;%1:-.2:.1;%.1:-.02:.02;
medianOrder = 5:5:50;
% for i = 1:length(medianOrder)
% %     c = ones(1,i)/i;
% %     f = filter(c, 1, force);
%    
% 
%     f = medfilt1(force,i);
%    %f = lowpass(force, f_filterArr(i)*2/Fs);
%    %f = filter(coeffWindow, 1, f);
%    %f = round(f);
%    plot(time, f + i*5); hold on;
% end
%ylim([240,340]);
%ylim([245,258]);
title("Force vs time", 'FontSize',18)
ylabel("force unit", 'FontSize',18)
xlabel("time (s)", 'FontSize',18)



% figure;
% set(gcf,'color','white')
% ax = gca(gcf);
% %plot(time, gradM); hold on;
% %plot(time, gradF); hold on;
% plot(time, gradForceLPFr); hold on;
% scatter(time(idxLocalMax), gradForceLPFr(idxLocalMax), 10, "black", 'filled'); hold on;   
% ylim([-1,5]);

a = filteredLPFr(idx4);
a = a(9:end-1,1);
%histogram(sort(diff(a)));
mean(diff(a))
