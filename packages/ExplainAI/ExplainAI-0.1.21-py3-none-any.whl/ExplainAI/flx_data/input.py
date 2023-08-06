import pandas as pd
from ..data_processing.data_processing_main import data_processing_main
import os
import pkgutil
import sys
def input_dataset(flag=0):
    if flag==0:

        # path=os.path.dirname(os.__file__)+"/site-packages/ExplainAI"
        # dir = os.path.dirname(os.path.abspath(os.__file__))
        # path =os.path.join("site-packages","ExplainAI")


        # path1 = os.getcwd()
        # print('path1',path1)
        #
        # path2=os.path.dirname(os.__file__)+"/site-packages/ExplainAI"
        # print('path2',path2)
        #
        # path3=os.path.dirname(sys.modules['ExplainAI'].__file__)
        #
        # print('path3',path3)

        path=os.path.dirname(sys.modules['ExplainAI'].__file__)
        file_name=os.path.join(path,'flx_data/','dataset.csv')
        print(file_name)
        data = pd.read_csv(file_name)



    elif flag==1:

        path = os.path.dirname(sys.modules['ExplainAI'].__file__)
        file_name = os.path.join(path, 'flx_data/', 'dataset_process.csv')

        data = pd.read_csv(file_name)


    elif flag==2:
        path = os.path.dirname(sys.modules['ExplainAI'].__file__)
        file_name = os.path.join(path, 'flx_data/', 'FLX_CN-Ha2_FLUXNET2015_FULLSET_DD_2003-2005_1-4.csv')


        data = pd.read_csv(file_name,header=0)

        d = data_processing_main(data=data,
                                 target='SWC_F_MDS_1',
                                 time_add=1,
                                 lag_add=1,
                                 elim_SM_nan=1,
                                 drop_ir=1,
                                 drop_nan_feature=1,
                                 part=0.7,
                                 n_estimator=10,
                                 sbs=True,
                                 split='2')
        data, ss = d.total()
    return data


