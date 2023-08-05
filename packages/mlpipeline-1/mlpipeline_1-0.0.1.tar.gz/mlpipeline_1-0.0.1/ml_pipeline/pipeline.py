import pandas as pd
import numpy as np
import os, re
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

def ml_pipeline(file_location, target_var, test_size):
    std_scaler = MinMaxScaler()
    df = pd.read_csv(file_location)
    list_giving_miss_count = str(df.isnull().sum()).split('\n')[:-1]
    new_list_miss = [re.split('\s{2,}', i) for i in list_giving_miss_count]
    missing_var_list = []
    index_of_threshold = []
    y = df[target_var]
    for i in range(len(new_list_miss)):
        if int(new_list_miss[i][1]) > 0:
            missing_var_list.append(new_list_miss[i][0])
    missing_percent = [df[i].isnull().sum()/df.shape[0]*100 for i in missing_var_list]
    for i in range(len(missing_percent)):
        if missing_percent[i] > 50:
            index_of_threshold.append(i)
    index_of_threshold = [i for i in range(len(missing_percent)) if missing_percent[i] > 50]
    new_list = [missing_var_list[i] for i in index_of_threshold]
    df.drop(columns = new_list, inplace = True)
    missing_less_50per = [i for i in missing_var_list if i not in new_list]
    dtype_missing_less_50per = [str(df[i].dtypes) for i in missing_less_50per]
    for i in range(len(missing_less_50per)):
        if dtype_missing_less_50per[i].__contains__('float') or dtype_missing_less_50per[i].__contains__('int'):
            df[missing_less_50per[i]].fillna(df[missing_less_50per[i]].mean(), inplace = True)
        elif dtype_missing_less_50per[i].__contains__('object'):
            df[missing_less_50per[i]].fillna(df[missing_less_50per[i]].mode()[0], inplace = True)
    column_list = df.columns.tolist()
    col_dtype_list = [str(df[i].dtypes) for i in column_list]
    int_flo_col_index = [i for i in range(len(col_dtype_list)) if col_dtype_list[i].__contains__('int') or col_dtype_list[i].__contains__('float')]
    col_with_int_flow = [column_list[i] for i in range(len(column_list)) if i in int_flo_col_index]
    col_not_contain_tar = [i for i in col_with_int_flow if i not in target_var]
    col_cat_type = [i for i in df.columns.tolist() if i not in col_with_int_flow]
    col_cat_type = [i for i in col_cat_type if i not in target_var]
    ############## Below line scale the numerical features #######################
    df[col_not_contain_tar] = std_scaler.fit_transform(df[col_not_contain_tar])
    ################# Below line encode the categorical variables ######################
    df1 = pd.get_dummies(df[col_cat_type])
    df.drop(columns = col_cat_type, inplace = True)
    df = pd.concat([df, df1], axis=1).reindex(df.index)
    X = df
    x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=test_size)
    return x_train, x_test, y_train, y_test

# X_train, X_test, y_train, y_test = ml_pipeline('tested.csv', 'Survived', 0.2)

# rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
# rf.fit(X_train, y_train)

# predicted = rf.predict(X_test)
# accuracy = accuracy_score(y_test, predicted)
# matrix = confusion_matrix(y_test, predicted)
# print(accuracy)
# print(matrix)