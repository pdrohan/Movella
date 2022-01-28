import pandas as pd
import numpy as np
import datetime as dt
import numpy as np
import webbrowser
import os 
import tabulate 

def return_dataframe_(path, show):
    '''1. This function reads a csv from the specified path location and optionally prints the first 5 rows
        2. note: openpyxl made this possible, csv was not parse correctly before installing it into the
        'movellatask virturalenv.
        3. Use shape to check if the import was successful
        Note: 'try' added to eliminate empty csv entry
    '''
    try:
        goalie_data = pd.read_csv(path)
        if show is True:
            print(goalie_data)
        return goalie_data
    except pd.errors.EmptyDataError:
        print('Note: filename.csv was empty. Please add a file with data')
        exit()
        


#Function used within other functions
def required_columns(dataframe, columns_needed):
    '''This was created from unit testing findings, ensure the columns required for a given function are
        in the dataframe provided to said function
        This code needs to be revisited, the sum / len statement is optimal
    '''
    #use this to return the actual dataframe needed
    # output = dataframe.columns.intersection(columns_needed)
    #return True if dataframe has teh columns
    output = dataframe.columns.isin(columns_needed)
    if len(columns_needed) == sum(np.array(output, dtype=bool)):
        return True
    else:
        return False

#Function used within other functions
def get_unique_val_in_col(df, col):
    '''Returns the number of unique values in the specified column
        Note: This may be a waste as it was not used as much as anticipated
    '''
    return df[col].nunique()

def format_df_columns(dataframe):
    '''Note 1: This is where I am 
        Jan 27: Added the required_columns function - need to clarify what is expected from Movella.
    '''
    #Check if the columns required for this calculaton exist in the dataframe provided
    if required_columns(dataframe=dataframe, columns_needed=['year', 'tmID']) is False:
        return print('The Dataframe Provided did not have the required columns')

    dataframe['year'] = pd.to_datetime(dataframe['year'], format='%Y') 
    #This changes it from datetime[ns] to a number again - unsure if he wants datatime because it includes
    #Months and days when that was not provided
    #not sure if he expects this or not
    # dataframe['year'] = dataframe['year'].dt.year
    dataframe['tmID'] = dataframe['tmID'].apply(str)
    return dataframe



def win_or_loss_agg_calc(dataframe, col):
    '''3. Wins_agg: total wins / total players & 4. Losses_agg: total losses / total players
    This is the 3rd & 4th task = sum(wins or losses)/countunique(players)
    need to drop or round to two decimals 
    updated to call get_unique_val_in_col
    updated to call required_columns, check if value is too high
    '''
    # all_col = col.append('playerID')
    #Check if the columns required for this calculaton exist in the dataframe provided
    if required_columns(dataframe=dataframe, columns_needed=[col, 'playerID']) is False:
        return print('The Dataframe Provided did not have the required columns')

    #Sum the column in question
    total_wins = dataframe[col].sum()
    #Call function to find the number of unique players
    count_of_players = get_unique_val_in_col(dataframe, 'playerID')
    f_string_name = 'loss Percentage'
    if col == 'W':
        f_string_name = 'win Percentage'

    wins_per_plyr = round(total_wins / count_of_players, 2)
    return f'The average {f_string_name} for all Goalies is {wins_per_plyr}%', wins_per_plyr
    # return wins_per_plyr



def agg_all_data(dataframe, col, req):
    '''Potential improvement: pass a list that is then aggregated instead of dropping columns 
        and calculated columns for no reason
    '''
    if required_columns(dataframe=dataframe, columns_needed=col) is False:
        return print('The Dataframe Provided did not have the required columns')

    dataframe = dataframe[col]
    output = dataframe.agg(req)
    return output 



def more_calcs(dataframe):
    '''5. GP_agg: total games played / total players
       6. Mins_over_GA_agg: total minutes played / total goals against
       7. GA_over_SA_agg: total goals against / total shots against
    '''
    #Check if the columns required for this calculaton exist in the dataframe provided
    if required_columns(dataframe=dataframe, columns_needed=['GP', 'playerID', 'Min','GA','SA']) is False:
        return print('The Dataframe Provided did not have the required columns')

    agg_data = agg_all_data(dataframe=dataframe, col=['GP', 'playerID', 'Min','GA','SA'], req=['sum'])
    #Games played average
    sum_of_games_played = agg_data.loc['sum']['GP']
    count_of_players = get_unique_val_in_col(dataframe, 'playerID')
    GP_agg = round(sum_of_games_played / count_of_players, 2)
    #Mins_over_GA_agg: total minutes played / total goals against
    total_mins_played = agg_data.loc['sum']['Min']
    total_goals_against = agg_data.loc['sum']['GA']
    Mins_over_GA_agg = round(total_mins_played / total_goals_against, 2)
    #GA_over_SA_agg: total goals against / total shots against
    total_shots_against = agg_data.loc['sum']['SA']
    GA_over_SA_agg = round(total_goals_against / total_shots_against * 100, 2)
    # return round(GP_agg, 2), round(Mins_over_GA_agg, 2), round(GA_over_SA_agg, 2)
    return f'The average games played is: {GP_agg}. The average minutes played per goal against is: {Mins_over_GA_agg} minutes. Goals against over shots against, as a percentage: {GA_over_SA_agg}%',\
        GP_agg, Mins_over_GA_agg, GA_over_SA_agg


def percent_games_won_byplayer(dataframe):
    '''The output dataframe here should have the same number of rows are the result of get_unique_val_in_col
    with the same df and col = playerID
    Note: Currently not a percent, just a decimal with too many decimals.
    jan 27: This was updated, now returning float for the win % column, 
            4 columns returned; playerID, W, GP, Win %
    '''
    #Check if the columns required for this calculaton exist in the dataframe provided
    if required_columns(dataframe=dataframe, columns_needed=['playerID','W', 'GP']) is False:
        return print('The Dataframe Provided to find the Percentage of Games Won for every Goalie did not have the required columns')

    output = dataframe[['playerID','W', 'GP']]
    output = output.groupby(['playerID']).sum()
    output = output[output['W'] != 0]
    output['Win %'] = round(output.apply(lambda row: row.W / row.GP * 100, axis=1), 2)
    output.reset_index(inplace=True)
    #Check if any percentage is greater than 100%
    if output['Win %'].all() > 100:
        return print('The dataframe provided may have incorrect data, please review the Win and Games Played columns')
    return output


def percent_games_won_byTeam(dataframe):
    '''percent of games won rate by team
    '''
    #Check if the columns required for this calculaton exist in the dataframe provided
    if required_columns(dataframe=dataframe, columns_needed=['tmID','W', 'GP']) is False:
        return print('The Dataframe Provided did not have the required columns')

    dff = dataframe[['tmID','W', 'GP']]
    output = dff.groupby(['tmID']).sum()
    output['Win Rate %'] = round(output.apply(lambda row: row.W / row.GP * 100, axis=1), 2)
    output.reset_index(inplace=True)
    return output



def most_goals_stopped(dataframe):
    '''Here I am assuming every value in the SA column is considered a goals_stopped
        9. most_goals_stopped: {‘playerID’: playerID, ‘goals_stopped’: goals_stopped}
            • Description: calculate goals stopped per player, then take the player with the max goals
                stopped and put the details in the dictionary
    '''
    #Check if the columns required for this calculaton exist in the dataframe provided
    if required_columns(dataframe=dataframe, columns_needed=['playerID','SA']) is False:
        return print('The Dataframe Provided did not have the required columns')

    output = dataframe[['playerID','SA']]
    output = output.groupby(['playerID']).sum().reset_index(drop=False)
    # print(output.head())
    max=output['SA'].idxmax()
    max_dict = {'playerID': output.iloc[max][0], 'goals_stopped': output.iloc[max][1]}
    return max_dict



def most_efficient(dataframe):
    '''Most efficient is defined as max(SA) / 
    10. most_efficient_player: {‘playerID’: playerID, ‘efficiency’: goals_stopped / minutes played}
        • Description: calculate the goals stopped per minute of play for each player, then take the
        player with the max efficiency just calculated and put the details in the dictionary
    '''
    #Check if the columns required for this calculaton exist in the dataframe provided
    if required_columns(dataframe=dataframe, columns_needed=['playerID','SA', 'Min']) is False:
        return print('The Dataframe Provided did not have the required columns')

    dff = dataframe[['playerID','SA', 'Min']]
    output = dff.groupby(['playerID']).sum().reset_index(drop=False)
    output = output.drop(output[output['SA'] == 0].index)
    # print(output)
    output['Efficiency'] = round(output.apply(lambda row: row.SA / row.Min * 100, axis=1), 2)
    max_efficiency = output['Efficiency'].idxmax()
    efficiency_dict = {'playerID': output.iloc[max_efficiency][0], 'efficiency': output.iloc[max_efficiency][3]}
    return efficiency_dict
    


'''When this file is run, we want all of the appropriate data to be printed, below will call the functions and
    return the data we want
'''
#This reads in the data 
path_to_csv = 'Goalies.csv'
df = return_dataframe_(path_to_csv, False)
df2 = format_df_columns(df)

print(' ')
print(' ')
print('Kaggle Data Goalie Analytics:')
#This returns the aggregated wins avg
win_string, w_numbr = win_or_loss_agg_calc(df2, 'W')
print('->', win_string)
#This returns the aggregated losses avg
print(' ')
loss_string, l_number = win_or_loss_agg_calc(df2, 'L')
print('->', loss_string)
print(' ')
# agg_data = agg_all_data(dataframe=df2, col=['GP'], req=['sum', 'min'])
#This calculates 5. GP_agg, Mins_over_GA_agg, GA_over_SA_agg
more_calcs_f_string, GP_agg, Mins_over_GA_agg, GA_over_SA_agg = more_calcs(df2)
print('->', more_calcs_f_string)
print(' ')
#This calculates the % of games won, grouped by goalie
print(percent_games_won_byplayer(df2).head().to_markdown())
print(' ')
#This calculates the % of games won, by team
print(percent_games_won_byTeam(df2).head().to_markdown())
print(' ')
#This returns a dictionary of the Goalie that stopped the most goals 
print('The Most Goals Stopped by any Goalie:')
most_stopped_dict = most_goals_stopped(df2)
print('->', most_stopped_dict)
print(' ')
#This returns the most efficient Goalie 
print('The Most Efficient Goalie: ')
most_efficient_dict = most_efficient(df2)
print('->', most_efficient_dict)

# Percent_Games_won_by_team = percent_games_won_byTeam(df2).to_html('Percent_Games_won_by_team.html')
# percent_games_won_by_plyr = percent_games_won(df2).to_html('Percent_Games_won_by_Player.html')
# # webbrowser.open('file://' + os.path.realpath('Percent_Games_won_by_team.html'))
# webbrowser.open('file://' + os.path.realpath('Percent_Games_won_by_Player.html'))


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


