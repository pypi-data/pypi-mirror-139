import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
import warnings

warnings.filterwarnings(action='ignore')
def get_null_percent(df):
    nan= (df.isnull().sum()*100/df.shape[0]).sort_values(ascending=False)
    percent=nan[nan != 0]
    data_types=df[percent.index].dtypes
    percent.name='percent'
    data_types.name='data type'
    return pd.merge(percent,data_types,left_index=True, right_index=True)


def insert(table,null_feature, algo):

    print('filling '+null_feature, end='')
    
    tbl=table

    tbl.loc[:,'internal_id']= np.arange(start=0,stop=tbl.shape[0], step=1)
    feat=pd.DataFrame(OrdinalEncoder().fit_transform(tbl.dropna(axis=1)), columns=tbl.dropna(axis=1).columns)
    rev_df=pd.concat([feat,tbl.loc[:,null_feature]], axis=1)
    
    rev_test=rev_df[rev_df.loc[:,null_feature].isnull()]
    
    rev_train=rev_df[rev_df.loc[:,null_feature].notnull()]

    print('...')
    #try:
    model=algo
    model.fit(rev_train.drop(['internal_id',null_feature], axis=1), rev_train.loc[:,null_feature])
    '''
    except:
        model=algo2
        model.fit(rev_train.drop(['internal_id',null_feature], axis=1), rev_train.loc[:,null_feature])
    '''
    #print(rev_test.drop(['internal_id',null_feature], axis=1).shape)
    
    rev_test.loc[:,null_feature]=model.predict(rev_test.drop(['internal_id',null_feature], axis=1))
    result=pd.concat([rev_train,rev_test],axis=0).sort_values(by='internal_id', ascending=True)[null_feature]
    #result=OrdinalEncoder().fit_transform(result.values.reshape(result.shape[0],1))
    tbl.loc[:,null_feature]=result
    return tbl.drop(['internal_id'], axis=1)



def fill(df, numeric_algorithm, categorical_algorithm):
    #get missing column and the percentage of missing values
    sor_flo=(df.isnull().sum()*100/df.shape[0]).sort_values()
    sor_flo=sor_flo[sor_flo != 0]
    sor_flo=sor_flo.index
    
    #labelencode the dataset
    cols= list(df.keys())
    for i in sor_flo:
        
        cols.remove(i)
        
    new_df=OrdinalEncoder().fit_transform(df.drop(sor_flo, axis=1))
    df.loc[:,cols]= pd.DataFrame(new_df, columns=cols)
    
    #print(sor_flo)
    
    #fill null values
    for i in sor_flo:
        if df[i].dtype == 'object':
            df= insert(df, i, categorical_algorithm)
            #print('object')
        else:
            df= insert(df, i, numeric_algorithm)
        
    return df


