from goalie_analytics.main import format_df_columns
import pytest
import pandas as pd

# def test_empty_slap():
#     assert format_df_columns is not None

def create_fake_df(numRows, numCols):
    output = pd.DataFrame(index=range(numRows),columns=range(numCols))
    return output

# tzz = create_fake_df(10, 5)
# print(tzz.shape)
# print(type(tzz.shape))

ttmz = create_fake_df(10, 4)
tmzz_shape = ttmz.shape

@pytest.mark.parametrize('test_input, expected', [
    ttmz, 1000
] )

def test_check_shape(test_input, expected):
    '''Ensure the dataframe returned from a function is the appropriate size 
    '''
    check_this = test_input.shape
    assert check_this == expected