function data=generateTrainData()
filename = 'E:\EOG removal software\eog_detection_result.mat';
data = importdata(filename);
segments = data.EOGs;

% manual = [
%     [26510, 26660];
%     ];

% manual = [
%      [468, 535];
%      [5632, 5704];
%      [11780, 11800];
%      [13300, 13570];
%      [26510, 26660];
%      ];
% manual = [
%      [520, 534];
%      [3185, 3205];
%      [26520, 26660];
%      ];
% manual = [
%      [520, 534];
%      [3185, 3205];
%      [13730, 13750];
%      [21910, 21920];
%      [28670, 28690];
%      ];
% manual = [
%     [1564,1589]
%      ];
manual = [
     ];

if data.isAdded == false
    segments = [segments
                manual;
               ];
    data.isAdded = true;
end

segments = sort(segments);
data.EOGs = segments;
save(filename, 'data');
data = data.data;

%len = 128;
len=128;
sP = 1;
seg = 1;
res = [];

while sP <= size(data, 2) - len + 1
    if seg <= size(segments, 1) 
        if sP <= segments(seg, 1) - len
            eP = sP + len - 1;
            res = [res 
                   data(1, sP : eP)];
            sP = eP + 1;
            fprintf('Add segment from %d to %d\n', sP, eP);
        else
            fprintf('Ignore segment from %d to %d\n', sP, segments(seg, 2));
            sP = segments(seg, 2) + 1;
            seg = seg + 1;
        end
    else
        eP = sP + len - 1;
            res = [res 
                   data(1, sP : eP)];
        sP = eP + 1;
        fprintf('Add segment from %d to %d\n', sP, eP);
    end
end

data = res';
save('traindata.mat', 'data');
end

function res = cmp(a, b)
    if a(1) > b(1) 
        res = 1;
        return;
    end
    if a(1) < b(1) 
        res = -1;
        return;
    end
    if a(2) > b(2) 
        res = 1;
        return;
    end
    if a(2) < b(2) 
        res = -1;
        return;
    end
    res = 0;
end

function res = sort(arr)
    res = arr;
    n = size(res, 1);
    for i = 1:n
        for j = i+1:n
            if cmp(res(i,:), res(j, :)) == 1
                tmp = res(i, :);
                res(i, :) = res(j, :);
                res(j, :) = tmp;
            end
        end
    end
end
