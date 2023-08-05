import pandas as pd
import numpy as np
from numba import jit
from scipy.signal import savgol_filter

@jit(nopython=True)
def extract_values_from_2d_array_with_row_col_numba(arr_2d_value, arr_row_col):
    '''
    Get pixel values for given 
    '''
    list_values = []
    for (row, col) in arr_row_col:
        list_values.append(arr_2d_value[row, col])

    return list_values




@jit(nopython=True)
def extract_values_from_3d_array_with_row_col_numba(arr_3d_value, arr_row_col):

    list_values = []
    for arr_2d_value in arr_3d_value:
        list_values.append(extract_values_from_2d_array_with_row_col_numba(arr_2d_value, arr_row_col))

    return np.array(list_values).T





def reformat_pixval(in_df, in_list_required_columns, dict_dtypes, default_dtype):
    '''
    Reformat a dataframe by reducing unrequired columns convert dtypes if specified in dict_dtypes and default_dtype.    
    '''
    out_df = in_df.reindex(columns=in_list_required_columns).copy()
        
    out_df['DANGER_TYPE_NAME'] = out_df['DANGER_TYPE_NAME'].fillna('')
    
    if dict_dtypes:
        out_df = convert_dtypes(out_df, dict_dtypes, default_dtype)
    
    return out_df
        

def get_list_pixval_col(in_df, re_pattern='t\\d+'):
    '''
    Get a list of column names of pixel values.
    '''
    list_pix_val_col = [col_nm for col_nm in in_df.columns if re.match(re_pattern, col_nm)]
    return list_pix_val_col
        

def apply_golay(arr_pixval, golay_window_length=9, golay_polyorder=5):
    '''
    Apply Savitzky-Golay filter
    '''
    
    print('Apply Savitzky-Golay filter')
    
    #temporary replace nan with --1e10
    arr_pixval = np.where(np.isnan(arr_pixval), -1e10, arr_pixval)    
    arr_pixval = savgol_filter(arr_pixval, window_length=golay_window_length, polyorder=golay_polyorder, axis=1)
        
    arr_pixval = np.where(arr_pixval < -1e5, np.nan, arr_pixval)

    return arr_pixval



@jit(nopython=True)
def get_cons_neg_cnt(in_arr, axis=1):
    '''
    Get max consecutive negative values count
    '''
    out_arr = np.max(
        np.cumsum(
            np.where(in_arr < 0, 1, 0),
            axis=axis
        ),
        axis=axis
    )
    
    return out_arr



@jit(nopython=True)
def get_neg_area_index(in_arr, axis=1):
    '''
    Get negative area index.
    Negative Area Index = Negative Area per All Area
    '''
    out_arr = np.sum(np.where(in_arr < 0, np.abs(in_arr), 0), axis=1) / np.sum(np.abs(in_arr), axis=1)
    
    return out_arr