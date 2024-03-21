% Note: input peaks is same size as data and has actual numerical values of 
% peaks of the data or grad of the data, with sign indicating rising or 
% falling edge. the output shiftedPeaks is an array of indices shifted 
% and has no values from the original signal. output shiftedpeaks
% cannot be the input peaks 

function [shiftedPeaksRising, shiftedPeaksFalling] = shiftPeaks(peaks, cutR, cutF)
    % rising edge
%     disp("Indices of Rising Peaks Before Shift")
%     disp(find(peaks>0))

     shiftedPeaksRising = find(peaks>0) + cutR;
    
%      disp("Indices of Rising Peaks After Shift")
%     disp(shiftedPeaksRising)

     %falling edge
%      disp("Indices of Falling Peaks Before Shift")
%      disp(find(peaks<0))

     shiftedPeaksFalling = find(peaks<0) + cutF;

%     disp("Indices of Falling Peaks After Shift")
%     disp(shiftedPeaksFalling)

     %shiftedPeaks = sort([shiftedPeaksRising; shiftedPeaksFalling]);
    
%     disp("Indices of All Peaks After Shift")
%     disp(shiftedPeaks)


    % I need to know if rising or falling edge
    % and potentially the original values
end