clear;
filename='1 WORKING\GIANG\L\GIANG-L01.mat';  
res=Find_1_v3(filename,false,1);    %channel 1 to 14  
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata01.mat','data_train')
save('data_EOG\testdata01.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,true,2);    %true shows the plot
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata02.mat','data_train')
save('data_EOG\testdata02.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,false,3);
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata03.mat','data_train')
save('data_EOG\testdata03.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,false,4);
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata04.mat','data_train')
save('data_EOG\testdata04.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,false,5);
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata05.mat','data_train')
save('data_EOG\testdata05.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,false,6);
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata06.mat','data_train')
save('data_EOG\testdata06.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,false,7);
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata07.mat','data_train')
save('data_EOG\testdata07.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,false,8);
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata08.mat','data_train')
save('data_EOG\testdata08.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,false,9);
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata09.mat','data_train')
save('data_EOG\testdata09.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,false,10);
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata10.mat','data_train')
save('data_EOG\testdata10.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,false,11);
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata11.mat','data_train')
save('data_EOG\testdata11.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,false,12);
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata12.mat','data_train')
save('data_EOG\testdata12.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,false,13);
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata13.mat','data_train')
save('data_EOG\testdata13.mat','EOGs', 'segments', 'data_test', 'oriSegments');

res=Find_1_v3(filename,false,14);
data_train=generateTrainData();
[EOGs, segments, data_test, oriSegments]=generateTestData();
save('data_EOG\traindata14.mat','data_train')
save('data_EOG\testdata14.mat','EOGs', 'segments', 'data_test', 'oriSegments');

fprintf('%s',filename);