function HaarData = haar(originData, level, number)
    [C,L] = wavedec(originData, level,'haar');
    test1 = waverec(C, L, 'haar', level);
    data = [];
    base = 2^level;
    for i=1:size(test1,2)
        for t = 1:base
            data = [data test1(i)];
        end
    end
    
    data1 = data;
    
    data1 = data1 * number;
    HaarData = data1';
    HaarData = HaarData(1:size(originData, 2), :);
end

