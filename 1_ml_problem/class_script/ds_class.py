###--- COMMON DATA PREP CLASS ---###
class com_data_prep:
    def __init__(self):
        print('Initialized common data prepration class')
        
    
    # Duplicate and All Null Removal
    def duplicate_null_remove(self,data,column=''):
        print('Before Dropping Duplicates and Null Rows:')
        print('rows: {}, columns: {}'.format(*data.shape))
        print('\nChecking Full Row Null Values:')
        print(data.isna().sum())
        print('\nDropping rows with all null values')
        data = data.dropna(how="all")
        if column == '':
            print('\nDropping duplicated rows based on all columns..')
            data = data.drop_duplicates()
        else:
            print('\nDropping Duplicated Rows based on column ', column)
            data = data.drop_duplicates(subset=column)
        print('\nAfter Dropping Duplicates and Null Rows:')
        print('rows: {}, columns: {}'.format(*data.shape))
        print()
        print()
        return data
    
    # Missing Values Threshold Removal
    def missing_remove(self,data,threshold=1.0):
        missing_props = data.isna().mean(axis=0)
        print('The threshold for filtering missing rows is at ', str(threshold*100), ' % missing rows')
        print('n\Columns and their missing row percentage are: ')
        print(missing_props)
        print('\nIdentifying columns with more than ', str(threshold*100),' % missing rows')
        over_threshold = missing_props[missing_props >= threshold]
        print(over_threshold)
        print('\nDropping coumns that exceeded the given threshold')
        data = data.drop(over_threshold.index, axis = 1)
        print('\nColumns left after dropping missing valued columns')
        print(data.columns)
        
        return data
    
    # Filling in Missing Values for Columns
    def fill_missing_val(self,data,int_val=0,str_val='NA',flt_val=0.0,iden_list=[]):
        print('Integer values to be filled is ',str(int_val))
        print('\nFloat values to be filled is ',str(flt_val))
        print('\nObject values to be filled is ',str_val)
        
        if len(iden_list) == 0:
            print('\nThere are no not-fill columns, all columns will be filled')
        else:
            print('\nColumns that would not be filled are :')
            print(iden_list)
        
        print('\nNumeric columns are ', data.select_dtypes(include="number").columns)
        print('\nNon-numeric columns are ',data.select_dtypes(exclude="number").columns)
        print()
        col_list = data.columns
        for item in col_list:
            if item in iden_list:
                print()
                print(item, ' is in not-fill list')
            elif "float" in data[item].dtypes.name:
                data[item] = data[item].fillna(flt_val)
                print(item, ' with column type ',data[item].dtypes,' has been filled with ',str(flt_val))
            elif "object" in data[item].dtypes.name:
                data[item] = data[item].fillna(str_val)
                print(item, ' with column type ',data[item].dtypes,' has been filled with ',str_val)
            elif "int" in data[item].dtypes.name:
                data[item] = data[item].fillna(int_val)
                print(item, ' with column type ',data[item].dtypes,' has been filled with ',str(int_val))
            else:
                print(item, ' has not been detected with any float, int or object data type..')
        return data
    
    # Converting columns to category..
    def convert_cat(self,series):
        return_series = series.astype('category')
        return return_series
    
    # Converting columns to integer..
    def convert_int(self,series):
        if series.dtypes.name == "object":
            series = series.fillna('0')
        return_series = series.astype('int64')
        return return_series
    
    # Displaying object columns unique values..
    def display_obj_cols(self,data):
        print('Note: display only object/categorical columns with at most 10 unique values..')
        print()
        
        not_ten = []
        
        col_list = data.select_dtypes(exclude="number").columns
        for col in col_list:
            if data[col].nunique() <= 10:
                print(col,' : ',data[col].unique())
                print('----------------------------------------------------------------------------')
            else:
                not_ten.append(col)
                
        if len(not_ten) != 0:
            print()
            print('Columns with more than 10 unique values are: ',not_ten)
        else:
            print()
            print('Note: all columns have unique values less than 10..')
            
        return
    
        # Displaying object columns unique values..
    def display_int_cols(self,data):
        print('Note: display only integer columns with at most 10 unique values..')
        print()
        
        not_ten = []
        
        col_list = data.select_dtypes(include="number").columns
        for col in col_list:
            if data[col].nunique() <= 10 and "int" in data[col].dtypes.name:
                print(col,' : ',data[col].unique())
                print('----------------------------------------------------------------------------')
            elif "int" in data[col].dtypes.name:
                not_ten.append(col)
            else:
                print()
                
        if len(not_ten) != 0:
            print()
            print('Columns with more than 10 unique values are: ',not_ten)
        else:
            print()
            print('Note: all columns have unique values less than 10..')
            
        return
    
    # Displaying columns with missing values > 50%..
    def display_null_val(self,data,more_50=True):
        missing_props = data.isna().mean(axis=0)
        if more_50:
            print('The threshold for missing rows to be displayed is 50% or more null values')
            over_threshold = missing_props[missing_props >= 0.5]
            print(over_threshold)
        else:
            print('All % are shown (excluding 0%)..')
            over_threshold = missing_props[missing_props > 0]
            print(over_threshold)
        
        return
    
    # Single Character Text Cleanning..
    def single_char_clean(self,series,old_char='',new_char='',lower_case=False,upper_case=False):   
        if lower_case == True and upper_case == True:
            print('Either lower or upper case can be true, but not simultaneously..')
            return
        
        if lower_case and old_char != '':
            print('Performing lower case and character replacement for this column..')
        elif upper_case and old_char != '':
            print('Performing upper case and character replacement for this column..')
        elif lower_case:
            print('Performing lower case only for this column..')
        elif upper_case:
            print('Performing lower case only for this column..')
        elif old_char != '':
            print('Performing character replacement only for this column..')
        else:
            print('Perhaps either make lower_case/upper_case = True or old_char=.. to use this function..')
            return
        
        new_list=[]
        for text in series:
            #replace intended character..
            if lower_case and old_char != '':
                text = text.replace(old_char, new_char).lower()
            elif upper_case and old_char != '':
                text = text.replace(old_char, new_char).upper()
            elif lower_case:
                text = text.lower()
            elif upper_case:
                text = text.upper()
            elif old_char != '':
                text = text.replace(old_char, new_char)
            else:
                text = text
            
            new_list.append(text)
        
        return new_list
    
    
    # Decile Ranking Function
    def decile_analysis_tab(self,decile_df,pd,np):
        base_response_rate = np.round(decile_df[decile_df.y == 1].shape[0]/decile_df.shape[0], decimals=8)
        print('Base_response_rate', base_response_rate)
        decile_df.sort_values(by='y_prob', inplace=True, ascending=False)
        decile_df.reset_index(inplace=True)
        decile_df['decile'] = np.nan
        d = int(np.ceil(decile_df.shape[0]/10))
        start = 0
        end = d
        for i in range(10):
            decile_df.loc[start:end, ['decile']] = i + 1
            start = start + d
            end = end + d
        qq = pd.crosstab(decile_df['decile'], decile_df['y'])
        qq.columns = ['zero','one']
        qq['min_prob'] = decile_df.groupby(by=['decile']).min()['y_prob']
        qq['max_prob'] = decile_df.groupby(by=['decile']).max()['y_prob']
        qq['count'] = decile_df.groupby(by=['decile']).count()['y_prob']
        qq['gain'] = np.round(100*qq['one']/qq['one'].sum(),decimals=2)
        qq['cum_gain'] = np.cumsum(qq['gain'])
        qq['lift'] = np.round((qq['one']/qq['count'])/base_response_rate,2)
        qq['actual'] = np.round(100*qq['one']/qq['count'],2)
        
        qq['cum_eventrate']=((qq.groupby(by=['decile']).sum()['one'])/qq['one'].sum()).cumsum()
        qq['cum_noneventrate']=((qq.groupby(by=['decile']).sum()['zero'])/qq['zero'].sum()).cumsum()
        qq['KS'] = np.round(qq['cum_eventrate']-qq['cum_noneventrate'], 3) * 100
        
        # Formating
        qq['cum_eventrate'] = qq['cum_eventrate'].apply('{0: .2%}'.format)
        qq['cum_noneventrate'] = qq['cum_noneventrate'].apply('{0: .2%}'.format)
        
        return qq
        
    # Show the Decile Ranking..
    def decile_show(self,prob_data,outcome_data,np,pd):
        y_pred_train = np.where(prob_data >= 0.5,1,0)
        df_y = pd.DataFrame()
        df_y['y'] = outcome_data.squeeze()
        df_y['y_prob'] = prob_data
        df_y['y_pred'] = y_pred_train
        qq = self.decile_analysis_tab(decile_df=df_y,pd=pd,np=np)
        print(qq)
        
        return    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
               
    
    
                
                
                
                
        