#----- 16th Feb 2022 -----#
#----- ZhangLe -----------#
#----- Data processing----#

from datetime import timedelta
import pandas as pd
import numpy as np

# 1. remove outlier
# tested
def remove_outlier(df, column_name, n_outlier=0.25):
    q1 = df[column_name].quantile(n_outlier)
    q3 = df[column_name].quantile(1 - n_outlier)
    iqr = q3 - q1
    lower_tail = q1 - 1.5 * iqr
    upper_tail = q3 + 1.5 * iqr
    print('lower_tail : ', lower_tail, '  upper_tail:', upper_tail)
    def remove_map(data):
        if data > float(upper_tail) or data < float(lower_tail):
            return n_outlier
        else:
            return data
    df['new'] = df[column_name].apply(remove_map)
    df = df.drop(columns = [column_name])
    df.rename(columns={'new': column_name}, inplace=True)
    return df

# 2. transform period
# tested
def add_period_to_time(df, date_column_name='DATE', period_column_name='PERIOD', period_minutes=30):
    df['DATE'] = pd.to_datetime(df[date_column_name], infer_datetime_format=True)
    def modify_period(data):
        mins = data[period_column_name] * period_minutes
        # print(type(data.DATE)) # for debug use
        new_date = data['DATE'] + timedelta(minutes = mins)
        return new_date
    df['data_label'] = df.apply(modify_period, axis=1)
    df['data_label'] = pd.to_datetime(df['data_label'], infer_datetime_format=True)
    df.drop(columns=[date_column_name, 'DATE'], inplace=True)
    df.rename(columns={ 'data_label': 'DATE' }, inplace=True)
    df['DATE'] = pd.to_datetime(df[date_column_name], infer_datetime_format=True)
    df = df.sort_values(by='DATE')
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    return df

# 3. split sequences for lstm/tcn/transformer model
def split_sequence(sequence, look_back = 30, look_forward = 30):
    X, y = list(), list()
    loop_len = sequence.shape[0]
    for i in range(1, loop_len):
        end_ix = i + look_back # fing the end of the x parten
        out_end_ix = end_ix + look_forward - 1
        if out_end_ix > loop_len:
            break
        seq_x, seq_y = sequence[i - 1 : end_ix-1,  :-1], sequence[end_ix-1 : out_end_ix, -1]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

