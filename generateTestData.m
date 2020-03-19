function [EOGs, segments, data, oriSegments]=generateTestData()
filename = 'E:\EOG removal software\eog_detection_result.mat';
data = importdata(filename);
segments = data.EOGs;

% Add additional segment manually
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
%%%

data = data.data;

%len = 128;
len=128;
sP = 1;
seg = 1;
EOGs = [];
segments1 = [];
oriSegments = [];

for index = 1:size(segments, 1)
    segment = segments(index, :);
    n_size = segment(2) - segment(1) + 1;
    if n_size > len
        continue
    end
%     oriSegments = [oriSegments
%                    segment];
    beforeAdded = 0;
    lastAdded = 0;
    if index - 1 > 0
        beforeAdded = segment(1) - segments(index - 1, 2) - 1;
    end
    
    if index + 1 < size(segments, 1)
        lastAdded = segments(index + 1, 1) - segment(2) - 1;
    else
        lastAdded = size(data, 2) - segment(2);
    end
    
    if beforeAdded + lastAdded + n_size < len
        continue
    end
    added = len - n_size;
    d = 0;
    c = 0;
    for fi = beforeAdded:-1:0
        la = added - fi;   
        if la <= lastAdded && la >= 0 
            d = segment(1) - fi;
            c = segment(2) + la;
            break;
        elseif la > lastAdded && fi==0
            break;
        end
    end
    
    if (d == 0 || c == 0)
        continue
    else
        oriSegments = [oriSegments
                   segment];
    end
    fprintf('Add segment from %d to %d\n', d, c);
    segments1 = [segments1
                [d, c]];
    EOGs = [EOGs
            data(1, d:c);
           ];
end

segments = segments1;
EOGs = EOGs';
save('testdata.mat', 'EOGs', 'segments', 'data', 'oriSegments');
%save(fullfile(tempdir,'testdata.mat', 'EOGs', 'segments', 'data', 'oriSegments' ))
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
