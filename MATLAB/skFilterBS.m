function y = skFilterBS(x)
%DOFILTER Filters input x and returns output y.

% MATLAB Code
% Generated by MATLAB(R) 9.13 and DSP System Toolbox 9.15.
% Generated on: 28-Dec-2024 04:27:20

%#codegen

% To generate C/C++ code from this function use the codegen command.
% Type 'help codegen' for more information.

persistent Hd;

if isempty(Hd)
    
    % The following code was used to design the filter coefficients:
    %
    % Fpass1 = 0.5;      % First Passband Frequency
    % Fstop1 = 1;        % First Stopband Frequency
    % Fstop2 = 4;        % Second Stopband Frequency
    % Fpass2 = 7;        % Second Passband Frequency
    % Apass1 = 1;        % First Passband Ripple (dB)
    % Astop  = 60;       % Stopband Attenuation (dB)
    % Apass2 = 1;        % Second Passband Ripple (dB)
    % Fs     = 32.1761;  % Sampling Frequency
    %
    % h = fdesign.bandstop('fp1,fst1,fst2,fp2,ap1,ast,ap2', Fpass1, Fstop1, ...
    %                      Fstop2, Fpass2, Apass1, Astop, Apass2, Fs);
    %
    % Hd = design(h, 'butter', ...
    %     'MatchExactly', 'passband', ...
    %     'SystemObject', true,...
    %      UseLegacyBiquadFilter=true);
    
    Hd = dsp.BiquadFilter( ...
        'Structure', 'Direct form II', ...
        'SOSMatrix', [1 -1.84693147634156 1 1 -0.467263914293863 ...
        0.744788647974915; 1 -1.84693147634156 1 1 -1.95802167977288 ...
        0.968786547640035; 1 -1.84693147634156 1 1 -1.89773187527982 ...
        0.908703207379205; 1 -1.84693147634156 1 1 -0.407604816486676 ...
        0.401119699824227; 1 -1.84693147634156 1 1 -1.8402233937688 ...
        0.85191609070136; 1 -1.84693147634156 1 1 -0.398818562020431 ...
        0.196221707915328; 1 -1.84693147634156 1 1 -1.79099607458655 ...
        0.803740325323703; 1 -1.84693147634156 1 1 -0.414225369016682 ...
        0.0827301668164014; 1 -1.84693147634156 1 1 -1.0974004751689 ...
        0.188349962330661], ...
        'ScaleValues', [0.766131143324053; 0.766131143324053; ...
        0.682073184758988; 0.682073184758988; 0.63082722108166; ...
        0.63082722108166; 0.603008625664472; 0.603008625664472; ...
        0.594174981165331; 1]);
end

s = single(x);
y = step(Hd,s);
