# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 15:03:36 2019

@author: Admin
"""
import scipy
from TestSAE import testing_SAE
from TrainSAE import training_SAE
import numpy as np
data_save=np.array([])
#name = 'THAO-L10'
i=int(input("Write a number 1-14: "))
#for i in range(6,7):
if i<10:
    testdata_loc='testdata0%d.mat'%(i)
    traindata_loc='traindata0%d.mat'%(i)
else: 
    testdata_loc='testdata%d.mat'%(i) 
    traindata_loc='traindata%d.mat'%(i)
    
training_SAE(traindata_loc)
fixed_data=testing_SAE(testdata_loc)
size_data=fixed_data.shape[0]
fixed_data=fixed_data.reshape(1,size_data)
#    if i==1:
#        data_save=fixed_data
#    else:
#        data_save=np.append(data_save,fixed_data,axis=0)
    
#filepath='E:\My Working Machine Learning\Clean Data\%s.mat' % name
#scipy.io.savemat(filepath,{'data':data_save})    
