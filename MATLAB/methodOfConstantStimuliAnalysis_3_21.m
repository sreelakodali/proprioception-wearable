% Method of constant stimuli analysis
close all;
% ------------ 2AFC, negative JND -----------------
data = [0.75, 9, 10; 0.5, 7, 10; 0.25, 5, 10]; % '2AFC, negative JND
options             = struct;   % initialize as an empty struct
options.sigmoidName = 'norm';   % choose a cumulative Gauss as the sigmoid  
options.expType     = '2AFC';   % choose 2-AFC as the experiment type  
                                % this sets the guessing rate to .5 (fixed) and  
                                % fits the rest of the parameters  
result = psignifit(data,options);
figure;
set(gcf,'color','white');
ax = gca(gcf);
plotPsych(result);
result.Fit(1)

% ------------ 2AFC, positive JND -----------------

data = [0.75, 8, 10; 0.5, 7, 10; 0.25, 4, 10]; % '2AFC, positive JND
options             = struct;   % initialize as an empty struct
options.sigmoidName = 'norm';   % choose a cumulative Gauss as the sigmoid  
options.expType     = '2AFC';   % choose 2-AFC as the experiment type  
                                % this sets the guessing rate to .5 (fixed) and  
                                % fits the rest of the parameters  
result = psignifit(data,options);
figure;
set(gcf,'color','white');
ax = gca(gcf);
plotPsych(result);
result.Fit(1)

% ------------ equalAsymptote -----------------

data = [-0.75, 1, 10; -0.5, 3, 10; -0.25, 5, 10; 0.25, 4, 10; 0.5, 4, 10; 0.75, 8, 10];
options             = struct;   % initialize as an empty struct
options.sigmoidName = 'norm';   % choose a cumulative Gauss as the sigmoid  
options.expType     = 'equalAsymptote';   % choose 2-AFC as the experiment type  
                                % this sets the guessing rate to .5 (fixed) and  
                                % fits the rest of the parameters  
result = psignifit(data,options);
figure;
set(gcf,'color','white');
ax = gca(gcf);
plotPsych(result);
%result.Fit(1)
threeFourthThresh = getThreshold(result, 0.75)
oneFourthThresh = getThreshold(result, 0.25)

JND = threeFourthThresh - oneFourthThresh
