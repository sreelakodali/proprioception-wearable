clc

i = 1;

subject_count = 1;

combinedTestAngles = [];

while 1

    prompt = "Do you want to enter a new subject (1/0)?";
    yes_no = input(prompt);

    if yes_no == 1

        subject_count = subject_count + 1;
    
        prompt = "Please enter subject number: ";
        subject_n = input(prompt);
        
        my_field = strcat('targetAngles_S',num2str(subject_n));
        prompt = "Please enter TargetAngle csv: ";
        csv = csvread(input(prompt));
        variable.(my_field) = csv;
        currentTargetAngles = csv;
        
        my_field = strcat('subjectAngles_S',num2str(subject_n));
        prompt = "Please enter SubjectAngle csv: ";
        csv = csvread(input(prompt));
        variable.(my_field) = csv;
        currentSubjectAngles = csv;
        % 
        my_field = strcat('angles_S',num2str(subject_n));
        variable.(my_field) = [ zeros(size(currentSubjectAngles,1),1)+subject_n currentTargetAngles currentSubjectAngles abs(currentTargetAngles - currentSubjectAngles)]; 
        % 1st column for subject number, 2nd column for target angles, 3rd column for subject attempt
        % angles, 4th column for abs error
        currentAngles = variable.(my_field);

        my_field = strcat('testAngles_S',num2str(subject_n)); 
        variable.(my_field) = [currentAngles(size(currentAngles,1)-40+1:size(currentAngles,1),1) ...
            currentAngles(size(currentAngles,1)-40+1:size(currentAngles,1),2) ...
            currentAngles(size(currentAngles,1)-40+1:size(currentAngles,1),3) ...
            currentAngles(size(currentAngles,1)-40+1:size(currentAngles,1),4)]; % now only taking the last 40 rows (test rows)
        currentTestAngles = variable.(my_field);

        prompt = "What was the first test case? 1 (H, NV) or 3 (NH, NV) "; % add 5th column for test case
        first_case = input(prompt);
        if first_case == 1
            currentTestAngles = [currentTestAngles(:,1) currentTestAngles(:,2) currentTestAngles(:,3) currentTestAngles(:,4) zeros([40 1]) zeros([40 1]) zeros([40 1])];
            for i = 1:10
                currentTestAngles(i,5) = 1; % 1's for (H, NV)
                currentTestAngles(i,6) = 1; % 1's for H
                currentTestAngles(i,7) = 0; % 0's for NV
            end
            for i = 11:20
                currentTestAngles(i,5) = 2; % 2's for (H, V)
                currentTestAngles(i,6) = 1; % 1's for H
                currentTestAngles(i,7) = 1; % 1's for V
            end 
            for i = 21:30
                currentTestAngles(i,5) = 3; % 3's for (NH, NV)
                currentTestAngles(i,6) = 0; % 0's for NH
                currentTestAngles(i,7) = 0; % 0's for NV
            end
            for i = 31:40
                currentTestAngles(i,5) = 4; % 4's for (NH, V)
                currentTestAngles(i,6) = 0; % 0's for NH
                currentTestAngles(i,7) = 1; % 1's for V
            end
        end
        if first_case == 3
            for i = 1:10
                currentTestAngles(i,5) = 3; % 3's for (NH, NV)
                currentTestAngles(i,6) = 0; % 0's for NH
                currentTestAngles(i,7) = 0; % 0's for NV
            end
            for i = 11:20
                currentTestAngles(i,5) = 4; % 4's for (NH, V)
                currentTestAngles(i,6) = 0; % 0's for NH
                currentTestAngles(i,7) = 1; % 1's for V
            end 
            for i = 21:30
                currentTestAngles(i,5) = 1; % 1's for (H, NV)
                currentTestAngles(i,6) = 1; % 1's for H
                currentTestAngles(i,7) = 0; % 0's for NV
            end
            for i = 31:40
                currentTestAngles(i,5) = 2; % 2's for (H, V)
                currentTestAngles(i,6) = 1; % 1's for H
                currentTestAngles(i,7) = 1; % 1's for V
            end
        end
        variable.(my_field) = currentTestAngles;

    end
    
    if yes_no == 0
           
           i = 0;
         
           break

    end

end




