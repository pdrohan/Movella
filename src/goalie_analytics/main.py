import pandas as pd
import numpy as np
import webbrowser
import os 
import tabulate 

def return_dataframe_(path, show):
    '''Error handling read_csv function
    '''
    try:
        goalie_data = pd.read_csv(path)
        if show is True:
            print(goalie_data)
        return goalie_data
    except pd.errors.EmptyDataError:
        print('Note: filename.csv was empty. Please add a file with data')
        exit()
        
def required_columns(dataframe, columns_needed):
    '''Determines if the dataframe passed has the columns passed
    '''
    output = dataframe.columns.isin(columns_needed)
    if len(columns_needed) == sum(np.array(output, dtype=bool)):
        return True
    else:
        return False

def format_df_columns(dataframe):
    '''Jan 27: Added the required_columns function - need to clarify what is expected from Mov
        Jan 31: Not necessary but nice to have 
    '''
    #Check if the columns required for this calculaton exist in the dataframe provided
    if required_columns(dataframe=dataframe, columns_needed=['year', 'tmID']) is False:
        return print('The Dataframe Provided did not have the required columns')

    dataframe['year'] = pd.to_datetime(dataframe['year'], format='%Y') 
    dataframe['tmID'] = dataframe['tmID'].apply(str)
    return dataframe

def get_unique_val_in_col(df, col):
    '''Returns the number of unique values in the specified column
        Note: This may be a waste as it was not used as much as anticipated
    '''
    return df[col].nunique()

def run_analytics(path_to_csv):
    '''This aggregates all of the desired stats and outputs a Pandas dataframe in HTML
    '''
    #Read in & Format
    df = return_dataframe_(path_to_csv, False)
    df2 = format_df_columns(df)

    if required_columns(dataframe=df2, columns_needed=['tmID','playerID','SA','Min','L','W', 'GP','GA','year']) is False:
        return print('The Dataframe Provided to find the Percentage of Games Won for every Goalie did not have the required columns')

    #Select the columns we need for the analysis
    output = df[['tmID','playerID','SA','Min','L','W', 'GP','GA','year']]
    #Group by team ID and year, and aggregate each column with the necessary calculations
    count_df = output.groupby(['tmID', 'year']).agg(['sum', 'count', 'nunique'])
    #Reset the index
    count_df.reset_index(inplace=True)
    #Declare new dataframe, the following is for team specific aggregations 
    final_df = pd.DataFrame()
    #Set the first two columns in new dataframe equal to the count_df columns
    final_df['tmID'] = count_df['tmID']
    final_df['year'] = count_df['year']
    #Calc wins_agg with values from count_df calculations
    #Total team wins for a specific year divided by the number of goalies they used that year
    final_df['Wins_agg'] = round(count_df['W']['sum'] / count_df['playerID']['nunique'], 2)
    #Total team losses for a specific year divided by the number of goalies that played for them that year
    final_df['Losses_agg'] = round(count_df['L']['sum'] / count_df['playerID']['nunique'], 2)
    #Total Games played by a team for a specific year divided by the number of goalies that played for them that year
    final_df['GP_Agg'] = round(count_df['GP']['sum'] / count_df['playerID']['nunique'],2)
    #The number of minutes the goalies played for a given team for a specific year divided by the number of goals allowed for that team that year 
    final_df['Mins_over_GA_agg'] = round(count_df['Min']['sum'] / count_df['GA']['sum'],2)
    #THe number of goals scored for a team over a given year divided by the number of shots against
    final_df['GA_over_SA_agg'] = round(count_df['GA']['sum'] / count_df['SA']['sum'] * 100,2)

    #This section calculates the player specific aggregations 
    player_df = pd.DataFrame()
    #Take the required columns, group by and sum 
    player_df = df[['tmID','playerID','L','W','GP','year','SA']].groupby(['playerID', 'tmID', 'year']).sum()
    #Reset index
    player_df.reset_index(inplace=True)
    #Add a column with that is a players win percentage for a given team for a given year
    player_df['Plyr Average Win Percentage'] = round(player_df['W'] / player_df['GP'] * 100, 2)
    #Join the previous dataframe with the player specific dataframe on the teamID and year 
    final_df = final_df.merge(player_df, how='left', on=['tmID','year'])

    #New dataframe, We previously calculated player % of games won, now need to find the mean at the 
    #Team level
    team_averages_df = player_df.groupby(['tmID', 'year']).mean().round(2)
    team_averages_df.reset_index(inplace=True)
    #Merge the new player win % rollup mean to the exisiting output dataframe
    final_df = final_df.merge(team_averages_df, how='left', on=['tmID','year'])
    #Rename the columns
    final_df = final_df.rename(columns={'Plyr Average Win Percentage_x':'Player Win Percentage','Plyr Average Win Percentage_y':'Player Win Percentage mean by Team'})

    #Select the columns that we want to display
    cols = ['tmID','year','playerID','Wins_agg','Losses_agg','GP_Agg','GA_over_SA_agg', 'Mins_over_GA_agg', 'Player Win Percentage','Player Win Percentage mean by Team']
    out_df = final_df[cols]

    return out_df

'''Functions called 
'''
path_to_csv = 'Goalies.csv'
out_df = run_analytics(path_to_csv)
#Send the dataframe to HTML to display more clearly
out_df.to_html('Aggregated Data 4 Kaggle Hockey Goalie DataSet.html')
webbrowser.open('file://' + os.path.realpath('Aggregated Data 4 Kaggle Hockey Goalie DataSet.html'))
df = return_dataframe_(path_to_csv, False)
df2 = format_df_columns(df)


#This is one of the two functions to output dictionaries
def most_goals_stopped(dataframe):
    '''Here I am assuming every value in the SA column is considered a goals_stopped
        9. most_goals_stopped: {‘playerID’: playerID, ‘goals_stopped’: goals_stopped}
            • Description: calculate goals stopped per player, then take the player with the max goals
                stopped and put the details in the dictionary
        
        This outputs a dictionary with the player with the most goals stopped
    '''
    #Check if the columns required for this calculaton exist in the dataframe provided
    if required_columns(dataframe=dataframe, columns_needed=['playerID','SA']) is False:
        return print('The Dataframe Provided did not have the required columns')

    #Select required column
    output = dataframe[['playerID','SA']]
    #Group by player ID, find sums and reset index
    output = output.groupby(['playerID']).sum().reset_index(drop=False)
    # print(output.head())
    max=output['SA'].idxmax()
    max_dict = {'playerID': output.iloc[max][0], 'goals_stopped': output.iloc[max][1]}
    return max_dict

#Output dictionary function
def most_efficient(dataframe):
    '''Most efficient is defined as max(SA) / 
    10. most_efficient_player: {‘playerID’: playerID, ‘efficiency’: goals_stopped / minutes played}
        • Description: calculate the goals stopped per minute of play for each player, then take the
        player with the max efficiency just calculated and put the details in the dictionary

        This outputs a dictionary with the player that was the most efficient 
    '''
    #Check if the columns required for this calculaton exist in the dataframe provided
    if required_columns(dataframe=dataframe, columns_needed=['playerID','SA', 'Min']) is False:
        return print('The Dataframe Provided did not have the required columns')

    #Select the required columns 
    dff = dataframe[['playerID','SA', 'Min']]
    #Sum by playerID and reset the index
    output = dff.groupby(['playerID']).sum().reset_index(drop=False)
    #Drop columns when SA = 0 because they cant be the most efficient, throws error
    output = output.drop(output[output['SA'] == 0].index)
    # Add a column, witch is Shots Against / Minutes played shown as a percentage
    output['Efficiency'] = round(output.apply(lambda row: row.SA / row.Min * 100, axis=1), 2)
    #Find the index of the row with the highest efficiency 
    max_efficiency = output['Efficiency'].idxmax()
    #Output the player ID and efficiency % as requested
    efficiency_dict = {'playerID': output.iloc[max_efficiency][0], 'efficiency': output.iloc[max_efficiency][3]}
    return efficiency_dict
    

'''This is the section that calls the dictionary functions and prints them
'''
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