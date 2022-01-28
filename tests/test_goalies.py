from goalie_analytics.main import return_dataframe_, format_df_columns, required_columns,\
     percent_games_won_byplayer, percent_games_won_byTeam, w_numbr, l_number, GP_agg,\
          Mins_over_GA_agg, GA_over_SA_agg, agg_all_data, df2, get_unique_val_in_col,\
               most_efficient_dict, most_stopped_dict

import pytest
import pandas as pd

@pytest.mark.parametrize('test_input', [
    'test_csvs/Goalies empty rows.csv',
    # this csv will trigger an error in test_df_is_none & test_df_has_columns, because it is empty
    # 'test_csvs/goalies empty',
    'test_csvs/Goalies missing columns.csv',
    #Will throw an assertion error for test_df_has_columns, because the necessary columns were deleted
    'test_csvs/Goalies missing key columns.csv',
    'test_csvs/Goalies unit test.csv'
] )

class TestParametrized:

    def test_df_is_none(self, test_input):
        '''Check if the dataframe returned from the given function is None
            if this test passes, the dataframe has data
            True and false make no difference     
        '''
        # df = return_dataframe_(test_input, False)
        df = return_dataframe_(test_input, True)
        assert df is not None

    def test_df_has_columns(self, test_input):
        '''Check if the required columns exist in the dataframe provided by return_dataframe_
            This by default checks if the dataframe is the right shape (column wise)
        '''
        df = return_dataframe_(test_input, False)
        check_value = required_columns(df, ['tmID','playerID','SA','Min','L','W', 'GP','GA','year'])
        assert check_value is not False
    
    def test_def_has_rows(self, test_input):
        '''Check if the dataframe imported has rows, and not just columns
        '''
        df = return_dataframe_(test_input, False)
        assert df.empty is False

    def test_column_data_types(self, test_input):
        '''Ensures the datatypes returned from the format_df_columns are correctly specified
            NOTE: this could change if the dtype is not 'Year' - need to check w/ mov.
        '''
        df = return_dataframe_(test_input, False)
        df2 = format_df_columns(df)
        assert df2.dtypes['tmID'] == 'object'
        assert df2.dtypes['year'] == 'datetime64[ns]'


@pytest.mark.parametrize('number_in, lower, upper', [
    (w_numbr, 0, 100),
    (l_number, 0, 100),
    (GP_agg, 0, agg_all_data(df2, ['GP'],['sum']).loc['sum']['GP']),
    (Mins_over_GA_agg, 0, 60),
    (GA_over_SA_agg, 0, 100), 
    (most_efficient_dict['efficiency'], 0, 100), 
    (most_stopped_dict['goals_stopped'], 0, 50000)
    
])

def test_output_number_bounds(number_in, lower, upper):
    '''simply checks the calculated value is within reasonable bounds
        This test assumes that this code will no longer be in production by the time someone reaches 
        50 000 shots against in the NHL. Current record is 31k.
    '''
    assert lower < number_in < upper


@pytest.mark.parametrize('dictn, key', [
    (most_efficient_dict, 'efficiency'), 
    (most_stopped_dict, 'goals_stopped')

])

def test_dictionary_outputs(dictn, key):
    assert dictn[key] is not None



@pytest.mark.parametrize('dataframe_in, expected_rows, col', [
    (df2, get_unique_val_in_col(df2, 'playerID'), 'playerID'),
    (df2, get_unique_val_in_col(df2, 'tmID'), 'tmID')
])

def test_output_dataframe(dataframe_in, expected_rows, col):
    '''The length of a column can not be longer than the number of unique rows, because these 
        two functinons being tested group by the specified column.
    '''
    if col == 'playerID':
        df_len = len(percent_games_won_byplayer(dataframe_in))
    if col == 'tmID':
        df_len = len(percent_games_won_byTeam(dataframe_in))
    assert df_len <= expected_rows


# print(df2.dtypes)
# @pytest.mark.parametrize('col, expected', [
#     ('tmID', df2.dtypes['tmID']),
#     ('playerID', object),
#     ('SA', 'float64'),
#     ('Min','float64'),
#     ('L','float64'),
#     ('W','float64'),
#     ('GP','float64'),
#     ('GA','float64'),
#     ('year','datetime64[ns]')
# ] )

# def test_column_data_types(col, expected):
#     '''NOTE: ensures the rows required are all there, 
#         i think i am on the right track but this nee
#     '''
#     assert df2.dtypes[col] is expected






# def test_empty_slap():
#     assert format_df_columns is not None


# def test_return_df(ds):
#     assert return_dataframe_ is not None
#     assert return_dataframe_.columns > 1


# def create_fake_df(numRows, numCols):
#     output = pd.DataFrame(index=range(numRows),columns=range(numCols))
#     return output

# ttmz = create_fake_df(10, 4)
# tmzz_shape = ttmz.shape


# def test_check_shape(test_input, expected):
#     '''Ensure the dataframe returned from a function is the appropriate size 
#     '''
#     check_this = test_input.shape
#     assert check_this == expected