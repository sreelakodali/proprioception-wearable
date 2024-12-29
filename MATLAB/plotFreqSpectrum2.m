function [Z, P1] = plotFreqSpectrum2(time, signal)

tdiff = diff(time);
Fs = 1/mean(tdiff);
disp(Fs);

fftY = fft(signal);
L = length(signal);

figure;
set(gcf,'color','white')
gca(gcf);
plot(time,signal);

magY = abs(fftY);
magYshift = abs(fftshift(fftY));

P2 = abs(fftY/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
Z = Fs/L*(0:(L/2));
%frequency spectrum 
figure;
set(gcf,'color','white')
gca(gcf);
plot(Fs/L*(0:(L/2)),P1,"LineWidth",3)
%ylim([0,2]);
title("Single-Sided Amplitude Spectrum of Signal (t)", 'FontSize',18);
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