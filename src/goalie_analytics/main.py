
# from cgi import test
# from doctest import OutputChecker
# from itertools import count
import pandas as pd
import numpy as np
import datetime as dt

# goalie_data = pd.read_csv(, sep='delimiter', header=0)
# df = pandas.read_csv(filepath, sep='delimiter', header=None)

# str(round(answer, 2))

def return_dataframe_(path, show):
    '''1. This function reads a csv from the specified path location and optionally prints the first 5 rows
        2. note: openpyxl made this possible, csv was not parse correctly before installing it into the
        'movellatask virturalenv.
        3. Use shape to check if the import was successful
    '''

    goalie_data = pd.read_csv(path)
    # print(goalie_data.shape)
    # print(goalie_data.iloc[0][3])
    # print(type(goalie_data.iloc[0][3]))
    # print(goalie_data.iloc[0][1])
    # print(type(goalie_data.iloc[0][1]))

    if show is True:
        print(goalie_data.head())
    return goalie_data

df = return_dataframe_('Goalies.csv', False)


def format_df_columns(data_frame, year_col, team_id_col):
    '''Note 1: This is where I am 
    '''
    data_frame[year_col] = pd.to_datetime(data_frame[year_col], format='%Y') 
    #This changes it from datetime[ns]
    data_frame[year_col] = data_frame[year_col].dt.year
    data_frame[team_id_col] = data_frame[team_id_col].apply(str)

    return data_frame


df2 = format_df_columns(df, 'year', 'tmID')
# print(df2.head())
# print(df2.dtypes)

def get_unique_val_in_col(df, col):
    return df[col].nunique()

def win_or_loss_agg_calc(dataframe, col, player_id_col):
    '''This is the 3rd & 4th task = sum(wins)/countunique(players)
    need to drop or round to two decimals 
    updated to call get_unique_val_in_col
    '''
    total_wins = dataframe[col].sum()
    # count_of_players = dataframe[player_id_col].nunique()
    count_of_players = get_unique_val_in_col(dataframe, player_id_col)

    wins_per_plyr = total_wins / count_of_players
    return wins_per_plyr


# print(win_or_loss_agg_calc(df2, 'W', 'playerID'))
# print(win_or_loss_agg_calc(df2, 'L', 'playerID'))




def agg_all_data(dataframe, col, req):
    '''Potential improvement: pass a list that is then aggregated instead of dropping columns 
    and calculated columns for no reason
    '''
    # dataframe = dataframe.drop(['playerID', 'tmID', 'lgID', 'year', 'stint'], axis =1 )
    # output = dataframe.agg(['count', 'size', 'nunique', 'max','min','sum', 'mean'])
    dataframe = dataframe[col]
    output = dataframe.agg(req)
    # print(type(output))
    return output 

# agg_data = agg_all_data(dataframe=df2, col='GA', req=['sum', 'min'])
# print(agg_data)

# print(agg_data.loc['sum']['GP'])

def more_calcs(dataframe):
    agg_data = agg_all_data(dataframe=dataframe, col=['GP', 'playerID', 'Min','GA','SA'], req=['sum'])
    #Games played average
    sum_of_games_played = agg_data.loc['sum']['GP']
    count_of_players = get_unique_val_in_col(dataframe, 'playerID')
    GP_agg = sum_of_games_played / count_of_players
    #Mins_over_GA_agg: total minutes played / total goals against
    total_mins_played = agg_data.loc['sum']['Min']
    total_goals_against = agg_data.loc['sum']['GA']
    Mins_over_GA_agg = total_mins_played / total_goals_against
    #GA_over_SA_agg: total goals against / total shots against
    total_shots_against = agg_data.loc['sum']['SA']
    GA_over_SA_agg = total_goals_against / total_shots_against
    return round(GP_agg, 2), round(Mins_over_GA_agg, 2), round(GA_over_SA_agg, 2)

# print(more_calcs(df2))

# 8. avg_percentage_wins: calculate the percentage of games won for each player, then take the
# mean at team level

def percent_games_won(dataframe):
    '''The output dataframe here should have the same number of rows are the result of get_unique_val_in_col
    with the same df and col = playerID
    Note: Currently not a percent, just a decimal with too many decimals.
    '''
    dff = dataframe[['playerID','W', 'GP']]
    output = dff.groupby(['playerID']).sum()
    output['Win %'] = output.apply(lambda row: row.W / row.GP, axis=1)

    return output
# print(percent_games_won(df2))

def percent_games_won_byTeam(dataframe):
    '''percent of games won rate by team
    '''
    dff = dataframe[['tmID','W', 'GP']]
    output = dff.groupby(['tmID']).sum()
    output['Win Rate'] = output.apply(lambda row: row.W / row.GP, axis=1)

    return output


# print(percent_games_won_byTeam(df2))

def most_goals_stopped(dataframe):
    '''Here I am assuming every value in the SA column is considered a goals_stopped
        9. most_goals_stopped: {‘playerID’: playerID, ‘goals_stopped’: goals_stopped}
            • Description: calculate goals stopped per player, then take the player with the max goals
                stopped and put the details in the dictionary
    '''
    dff = dataframe[['playerID','SA']]
    output = dff.groupby(['playerID']).sum().reset_index(drop=False)
    # print(output.head())
    max=output['SA'].idxmax()
    max_dict = {'playerID': output.iloc[max][0], 'goals_stopped': output.iloc[max][1]}
    return max_dict

# print(most_goals_stopped(df2))

def most_efficient(dataframe):
    '''Most efficient is defined as max(SA) / 
    10. most_efficient_player: {‘playerID’: playerID, ‘efficiency’: goals_stopped / minutes played}
        • Description: calculate the goals stopped per minute of play for each player, then take the
        player with the max efficiency just calculated and put the details in the dictionary
    '''
 
    dff = dataframe[['playerID','SA', 'Min']]
    output = dff.groupby(['playerID']).sum().reset_index(drop=False)
    output = output.drop(output[output['SA'] == 0].index)
    # print(output)
    output['Efficiency'] = output.apply(lambda row: row.SA / row.Min, axis=1)
    max_efficiency = output['Efficiency'].idxmax()
    efficiency_dict = {'playerID': output.iloc[max_efficiency][0], 'efficiency': output.iloc[max_efficiency][3]}
    return efficiency_dict
    
# print(most_efficient(df2))



'''
playerID     object
year          int64
stint         int64
tmID         object
lgID         object
GP          float64
Min         float64
W           float64
L           float64
T/OL        float64
ENG         float64
SHO         float64
GA          float64
SA          float64
PostGP      float64
PostMin     float64
PostW       float64
PostL       float64
PostT       float64
PostSHO     float64
PostGA      float64
PostSA      float64'''

'''

Assessment Task:
Program and display these aggregates as output
1. tmID: string
2. year: Year
3. Wins_agg: total wins / total players
4. Losses_agg: total losses / total players
5. GP_agg: total games played / total players
6. Mins_over_GA_agg: total minutes played / total goals against
7. GA_over_SA_agg: total goals against / total shots against
8. avg_percentage_wins: calculate the percentage of games won for each player, then take the
mean at team level
9. most_goals_stopped: {‘playerID’: playerID, ‘goals_stopped’: goals_stopped}
• Description: calculate goals stopped per player, then take the player with the max goals
stopped and put the details in the dictionary
10. most_efficient_player: {‘playerID’: playerID, ‘efficiency’: goals_stopped / minutes played}
• Description: calculate the goals stopped per minute of play for each player, then take the
player with the max efficiency just calculated and put the details in the dictionary
'''


