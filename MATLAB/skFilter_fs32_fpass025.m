function y = skFilter_fs32_fpass025(x)
%DOFILTER Filters input x and returns output y.

% MATLAB Code
% Generated by MATLAB(R) 9.13 and DSP System Toolbox 9.15.
% Generated on: 28-Dec-2024 03:58:08

%#codegen

% To generate C/C++ code from this function use the codegen command.
% Type 'help codegen' for more information.

persistent Hd;

if isempty(Hd)
    
    % The following code was used to design the filter coefficients:
    %
    % Fpass = 0.25;     % Passband Frequency
    % Fstop = 6;        % Stopband Frequency
    % Apass = 1;        % Passband Ripple (dB)
    % Astop = 80;       % Stopband Attenuation (dB)
    % Fs    = 32.1761;  % Sampling Frequency
    %
    % h = fdesign.lowpass('fp,fst,ap,ast', Fpass, Fstop, Apass, Astop, Fs);
    %
    % Hd = design(h, 'butter', ...
    %     'MatchExactly', 'passband', ...
    %     'SystemObject', true,...
    %      UseLegacyBiquadFilter=true);
    
    Hd = dsp.BiquadFilter( ...
        'Structure', 'Direct form II', ...
        'SOSMatrix', [1 2 1 1 -1.93708090399339 0.940707323287745; 1 1 0 1 ...
        -0.940653519482245 0], ...
        'ScaleValues', [0.000906604823587526; 0.0296732402588777; 1]);
end

s = single(x);
y = step(Hd,s);

