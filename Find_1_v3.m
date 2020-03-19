function res = Find_1_v3(filename, isPloted,index)
    %index is the number of chosen channel 
    init(isPloted)
    findEOG(filename,index);
    global total detail
    fprintf('Total number of EOG: %d\n', total);
    res = total;
    save('E:\EOG removal software\eog_detection_result.mat', 'detail'); 
end 

function init(bool)
    global thresholds level base ComArr mark total isPloted data detail
    thresholds = [3.8; 3.9; 3.3; 3.19; 100; 100; 100; 100; 100; 100];
    %thresholds = [3.8; 3.9; 3.80; 3.73; 3.6; 3.5; 100; 100; 100; 100];
    level = 4; 

    base = 2^(level);

    ComArr = [];
    
    mark = [];
    
    total = 0;
    
    isPloted = bool;
    data = [];
    detail = struct;
    detail.EOGs = [];
    detail.isAdded = false;
end

function data = loadData(filename,index)
    data = importdata(filename);
%     i = 18;
%     data = data(1, (i - 1) * 10 * 128 + 1: (i) * 10 * 128);
    data = data(index, :);
    len = size(data);
    len = len(2);
    len = floor(len / 2) * 2;
    data = data(1, 1:len);
end

function comArr = compactArray(arr)
    len = size(arr(:,1));
    len = len(1);
    global base n
    global segment mark
    n = 0;
    comArr = zeros(floor((len - 1) / base + 1), 1);
    mark = zeros(floor((len - 1) / base + 1), 1);
    segment = zeros(floor((len - 1) / base + 1) * 10, 2);
    for i = 1:base:len
        comArr(floor((i - 1) / base + 1)) = arr(i); 
    end
end

function [maxDis, minDis, avgDis, sl] = calc(arr, oldSum, oldSl)
    minVal = min(arr);
    maxVal = max(arr);
    
    maxDis = -1;
    minDis = maxVal - minVal;
    avgDis = oldSum;
    sl = oldSl;
    
    global mark
    len = size(arr);
    len = len(1);
    for i = 2:len
        if mark(i) == 1 || mark(i - 1) == 1
            continue
        end
        if i > 1
           sl = sl + 1;
           dis = abs(arr(i) - arr(i - 1));
           avgDis = avgDis + dis;
           maxDis = max(maxDis, dis);
           if dis > 0
               minDis = min(minDis, dis);
           end
        end
    end
    %disp(avgDis);
    %disp(len);
    avgDis = avgDis / sl;
end

function plotLine(x, y)
    global isPloted
    if isPloted
        plot(x, y, 'g');
    end
end

function bool5 = isAccpeted(sPoint, ePoint)
    bool5 = true;
    global mark
    for j = sPoint:ePoint
        if mark(j) == 1 && j ~= sPoint && j ~= ePoint
            bool5 = false;
        end
    end
end

function determineEOG(arr, length, threshold, sP)
    len = size(arr);
    len = len(1); 
    sPoint = 1;
    global segment n
    while sPoint < len
        ePoint = sPoint + length - 1;
        %fprintf('from %d to %d :', sPoint, ePoint);
        if ePoint > len
            break
        end
        
        if ~isAccpeted(sPoint, ePoint)
            sPoint = sPoint + 1;
            continue
        end
        
        arrP = arr(sPoint:ePoint);
        
        if check(arrP, sPoint, ePoint, sP)
            %disp('Accept');
            %fprintf('check1: from %d(%d) to %d(%d)\n', sPoint, (sPoint - 1) * base + 1, ePoint, (ePoint - 1) * base + 1);
            %disp(arrP);
            %check arrP is EOG or Not
            %if sPoint == 267
            %    disp('ok');
            %end
            if check2(arrP, threshold)
                n = n + 1;
                segment(n, :) = [sPoint ePoint];
                %fprintf('check2: from %d(%d) to %d(%d)\n', sPoint, (sPoint - 1) * base + 1, ePoint, (ePoint - 1) * base + 1);
                %fprintf(arrP);
                %disp('EOG');
                sPoint = ePoint - 1;
            end
        end           
        sPoint = sPoint + 1;
    end
    %break;
end

% Draw 2 line to detect where EOGs locate
function drawEOG(sP)
    global base b1 segment n mark total detail
    segment = segment(1:n, :);
    segment = sort(segment);
    sPoint = 0;
    ePoint = 0;
    res = 0;
    for i = 1:n
        d = segment(i, 1);
        c = segment(i, 2);
        if d <= ePoint + 1
            ePoint = c;
        else
            %Plot
            if sPoint > 0
                a1 = [sP + (sPoint - 1) * base + 1 sP + (sPoint - 1) * base + 1];
                plotLine(a1, b1);
                a1 = [sP + (ePoint) * base sP + (ePoint) * base];
                plotLine(a1, b1);
                res = res + 1;
                
                for j = sPoint:ePoint
                    mark(j) = 1;
                end
                detail.EOGs = [detail.EOGs
                    [sP + (sPoint - 1) * base + 1 sP + (ePoint) * base]];
            end
            %new segment
            sPoint = d;
            ePoint = c;
        end
        %a1 = [(d - 1) * base + 16 (d - 1) * base + 16];
        %plotLine(a1, b1);
        %a1 = [(c - 1) * base + 16 (c - 1) * base + 16];
        %plotLine(a1, b1);
    end
    %Plot 
    if sPoint > 0
        a1 = [sP + (sPoint - 1) * base + 1 sP + (sPoint - 1) * base + 1];
        plotLine(a1, b1);
        a1 = [sP + (ePoint) * base sP + (ePoint) * base];
        plotLine(a1, b1);
        res = res + 1;
        for j = sPoint:ePoint
            mark(j) = 1;
        end
        detail.EOGs = [detail.EOGs
                    [sP + (sPoint - 1) * base + 1 sP + (ePoint) * base]];
    end
    
    fprintf('Number of EOG: %d\n', res);
    total = total + res;
end

% segmentation?
function data = getSubData(originData, sP, eP)
    len = size(originData);
    len = len(2);
    data = originData(1, sP:min(eP, len));
    len = size(data);
    len = len(2);
    len = floor(len / 2) * 2;
    data = data(1, 1:len);
end

function subFindEOG(originData, sP, eP)
    len = size(originData);
    len = len(2);
    if (min(eP, len) - sP + 1) < 32
        return
    end
    data = getSubData(originData, sP, eP);
    %using Haar Wavelet, decompose at level 'level' and reconstruct at 
    %'level-1'
    global level
    
    HaarEEG = haar(data, level, 0.25);
    %[a, d] = haart(data, level);
    %HaarEEG = ihaart(a, d, level - 2);
    
    %get some info from data after reconstruct
    minVal = min(HaarEEG);
    maxVal = max(HaarEEG);
    tb = (maxVal - minVal) / 2;
    %fprintf('Min Value: %f\n', minVal);
    %fprintf('Max Value: %f\n', maxVal);
    global b1
    b1 = [minVal - tb maxVal + tb];

    %draw pure EEG data and Haar Wavelet data
    %figure
    %plot(data)
    %hold on
    %plot(HaarEEG)

    %Generate compact array from HaarEEG
    global ComArr avgDis thresholds n oldSum oldSl
    ComArr = compactArray(HaarEEG);
    
    tmp_oldSl = oldSl;
    
    times = 10;
    for t = 1:times
        %Calc max, min, avg of distance
        
        [maxDis, minDis, avgDis, tmp_oldSl] = calc(ComArr, oldSum, oldSl);

        %fprintf('Max Distance: %f\n', maxDis);
        %fprintf('Min Distance: %f\n', minDis);
        %fprintf('AVG Distance: %f\n', avgDis);

        %Loop for find EOG
        %length from 19 - 55 = (3 - 5)
        length = 4;
  
        n = 0;
        for len = length:-1:3
            %fprintf('Length is %d\n', len);
            determineEOG(ComArr, len, thresholds(t), sP);
        end

        drawEOG(sP);
    end
   
    oldSum = avgDis * tmp_oldSl;
    oldSl = tmp_oldSl;
end

function findEOG(filename,index)
    %load data
    global data detail
    data = loadData(filename,index);
    detail.data = data;
    %using Haar Wavelet, decompose at level 'level' and reconstruct at 
    %'level-1'
    global level
    
    HaarEEG = haar(data, level, 1 / (sqrt(2) ^ level));
    %[a, d] = haart(data, level);
    %HaarEEG = ihaart(a, d, level - 2);
    
    %get some info from data after reconstruct
    minVal = min(HaarEEG);
    maxVal = max(HaarEEG);
    tb = (maxVal - minVal) / 2;
    %fprintf('Min Value: %f\n', minVal);
    %fprintf('Max Value: %f\n', maxVal);
    global b1 avgDis oldSum oldSl isPloted
    b1 = [minVal - tb maxVal + tb];

    %draw pure EEG data and Haar Wavelet data
    d=10000;
    c=26500;
    if isPloted
        figure
        plot(data)
        hold on
%         plot(HaarEEG)
%         hold on
    end
    
    avgDis = 0;
    oldSum = 0;
    oldSl = 0;
    step = 1600;
    len = size(data);
    len = len(2);
    startP = 1;
    while startP < len 
        endP = startP + step;
        if endP > len
            subFindEOG(data, startP, len)
            break
        end
        subFindEOG(data, startP, endP)
        startP = endP - 32;
    end
end
%  ???
function bool3 = isInHeightUp(sP, eP)
    lowerbound = 35.7;
    upperbound = 1000.0;
    
    global data
    subData = getSubData(data, sP, eP);
    
    maxHeight = max(subData);
    
    bool3 = maxHeight >= lowerbound && maxHeight <= upperbound;
end
%???
function bool4 = isInHeightDown(sP, eP)
    lowerbound = -500;
    upperbound = -77.3;
    
    global data
    subData = getSubData(data, sP, eP);
    
    minHeight = min(subData);
    
    bool4 = minHeight >= lowerbound && minHeight <= upperbound;
end

%compare ?
function bool = check(arr, sP, eP, start)
    len = size(arr);
    len = len(1);
    %disp(len);
    bool = true;
    if ~((arr(1) <= arr(2) && arr(len - 1) >= arr(len)) || (arr(1) >= arr(2) && arr(len - 1) <= arr(len)))
        bool = false;
        return
    end
    global avgDis base
    if abs(arr(2) - arr(1)) <= 2.0 * avgDis || abs(arr(len - 1) - arr(len)) <= 2.0 * avgDis 
        bool = false; 
        return
    end
    
    if max(abs(arr(2) - arr(1)), abs(arr(len - 1) - arr(len))) / min(abs(arr(2) - arr(1)), abs(arr(len - 1) - arr(len))) >= 4.0
        bool = false;
        return
    end
    if arr(1) <= arr(2)
        status = 1;
        for i = 2:len
            dis = arr(i) - arr(i - 1);
            if status == 1
                if dis <= 0
                    if ~isInHeightUp(start + sP * base - 1, start + eP * base - 1)
                        bool = false;
                    end
                    status = -1;
                end
            else
                if dis >=0
                    bool = false;
                    break;
                end
            end
        end
    else
        status = -1;
        for i = 2:len
            dis = arr(i) - arr(i - 1);
            if status == -1
                if dis >= 0
                    if ~isInHeightDown(start + sP * base - 1, start + eP * base - 1)
                        bool = false;
                    end
                    status = 1;
                end
            else
                if dis <=0
                    bool = false;
                    break;
                end
            end
        end
    end
end
%compare the wavelet trnsform to threshold
function bool2 = check2(arr, threshold)
    len = size(arr);
    len = len(1);
    bool2 = false;
    
    maxDis = -1;
    minDis = max(arr) - min(arr);
    avg = 0;
    global avgDis
      
    for i = 2:len
        if i > 1
            dis = abs(arr(i) - arr(i - 1));
            avg = avg + dis;
            maxDis = max(maxDis, dis);
            if dis > 0
                minDis = min(minDis, dis);
            end
        end
    end
    avg = avg / (len - 1);
    %check
%     if minDis > 2.05 * avgDis
%         bool2 = true;
%     end
    
    if avg > threshold * avgDis
        bool2 = true;
    end
    if bool2 == true
        %fprintf('Max Distance: %f\n', maxDis);
        %fprintf('Min Distance: %f\n', minDis);
        %fprintf('AVG Distance: %f\n', avg);
    end
end
