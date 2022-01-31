from ctypes import util
from goalie_analytics.main import return_dataframe_, format_df_columns, df2,\
               most_efficient_dict, most_stopped_dict,path_to_csv, out_df, run_analytics
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal, assert_index_equal
import datatest as dt 
from datatest import validate


'''Welcome to the test file, I have tests for every function and I even made some fake csvs, to create
    tests for unique csv files. 
    If you want some tests to fail, un-comment the code on lines 17, 19, 20, 22, 23
'''

@pytest.mark.parametrize('test_input', [
    # 'test_csvs/Goalies empty rows.csv',
    # # this csv will trigger an error in test_df_is_none & test_df_has_columns, because it is empty
    # 'test_csvs/goalies empty',
    # 'test_csvs/Goalies missing columns.csv',
    # # Will throw an assertion error for test_df_has_columns, because the necessary columns were deleted
    # 'test_csvs/Goalies missing key columns.csv',
    # 'test_csvs/Goalies unit test.csv',
    path_to_csv
] )

class TestParametrized:

    @pytest.mark.mandatory
    def test_df_correct_size(self, test_input):
        '''This is the use of assert_dataframe_equals as requested 
           Checks if the return_dataframe_ function read in the data as expected
        '''
        df = return_dataframe_(test_input, False)
        csv_df = pd.read_csv(test_input)
        assert_frame_equal(csv_df, df, check_dtype=True)

    @pytest.mark.mandatory
    def test_columns(self, test_input):
        '''Ensures the csvs dataframe columns match the required columns 
        '''
        df = return_dataframe_(test_input, False)

        dt.validate(
            df.columns,{'playerID','year','stint','tmID','lgID','GP','Min',	'W','L','T/OL','ENG',\
                'SHO','GA','SA','PostGP','PostMin','PostW','PostL','PostT','PostENG','PostSHO',\
                    'PostGA','PostSA'}
        )
    
    @pytest.mark.mandatory
    def test_output_df(self, test_input):
        '''Check if the outputted value from run_analytics has the right columns 
        '''
        out_cols = run_analytics(test_input).columns
        requirement = {'tmID','year','playerID','Wins_agg','Losses_agg','GP_Agg','GA_over_SA_agg', 'Mins_over_GA_agg', 'Player Win Percentage','Player Win Percentage mean by Team'}
        dt.validate(out_cols, requirement)

    def test_check_indexes(self, test_input):
        '''The indexes in the input csv and the output csv should be the same,
            when accounting for the duplicate values
        '''
        out_df_i = run_analytics(test_input).index
        # print(out_df)
        in_df = return_dataframe_(test_input, False)
        #If there is duplicate values, grouped by 'tmID','playerID','year' they will be aggregated
        #in the output dataframe from run_analytics, therefore drop them to find the correct index
        no_duplicates = in_df.drop_duplicates(subset=['tmID','playerID','year'])
        # print(in_df)
        assert_index_equal(out_df_i, no_duplicates.index, exact='equiv', check_exact=False, rtol=3)

    @pytest.mark.mandatory
    def test_df_is_none(self, test_input):
        '''Check if the dataframe returned from the given function is None
            if this test passes, the dataframe has data
            True and false make no difference     
        '''
        # df = return_dataframe_(test_input, False)
        df = return_dataframe_(test_input, False)
        assert df is not None

    @pytest.mark.mandatory
    def test_def_has_rows(self, test_input):
        '''Check if the dataframe imported has rows, and not just columns
        '''
        df = return_dataframe_(test_input, False)
        assert df.empty is False
    
    @pytest.mark.mandatory
    def test_column_data_types(self, test_input):
        '''Ensures the datatypes returned from the format_df_columns are correctly specified
            NOTE: this could change if the dtype is not 'Year' - need to check w/ mov.
        '''
        df = return_dataframe_(test_input, False)
        df2 = format_df_columns(df)
        assert df2.dtypes['tmID'] == 'object'
        assert df2.dtypes['year'] == 'datetime64[ns]'
    

@pytest.mark.parametrize('dictn, key', [
    (most_efficient_dict, 'efficiency'), 
    (most_stopped_dict, 'goals_stopped')

])

@pytest.mark.mandatory
def test_dictionary_outputs(dictn, key):
    '''Asserts the dictionary functions are outputting values 
    '''
    assert dictn[key] is not None
