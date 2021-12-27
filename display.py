from mplsoccer.pitch import Pitch, VerticalPitch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch, Arc
from matplotlib.font_manager import FontProperties
from plotly.offline import init_notebook_mode,iplot
from PIL import Image

init_notebook_mode(connected=True)
pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None


def open_fifa_version_df(fifa_version):
    df = pd.read_csv('./data/display/players_' + str(fifa_version) + '.csv', low_memory = False, encoding='gbk')
    df['fifa_version'] = int(fifa_version)
    new_cols_order = ['fifa_version'] + df.columns.to_list()[:-6] # removing picture URLs
    df = df[new_cols_order]
    return df


# players_df = pd.DataFrame()
# for fifa_version in range(15, 23): # upper bound excluded from range
#     players_df = players_df.append(open_fifa_version_df(fifa_version))
#
# players_df.to_csv('./data/display/players_all.csv', index=False)
# print(len(players_df))
# players_df.head(5)

players_df = pd.read_csv('players_all_simple.csv', low_memory=False)

# adding the 'best_position' and 'value_million_eur' fields to each df
def add_position_and_value_fields(input_df):
    input_df['best_position'] = input_df['player_positions'].str.split(',').str[0]
    # about 1k players through all FIFA versions have no values associated - the NaN 'value_eur' values are replaced with 0
    input_df['value_eur'] = input_df['value_eur'].fillna(0)
    input_df['value_million_eur'] = pd.to_numeric(input_df['value_eur'], errors='coerce') / 1000000
    return input_df


players_df = add_position_and_value_fields(players_df)
df15 = add_position_and_value_fields(players_df[players_df['fifa_version'] == 15])
df16 = add_position_and_value_fields(players_df[players_df['fifa_version'] == 16])
df17 = add_position_and_value_fields(players_df[players_df['fifa_version'] == 17])
df18 = add_position_and_value_fields(players_df[players_df['fifa_version'] == 18])
df19 = add_position_and_value_fields(players_df[players_df['fifa_version'] == 19])
df20 = add_position_and_value_fields(players_df[players_df['fifa_version'] == 20])
df21 = add_position_and_value_fields(players_df[players_df['fifa_version'] == 21])
df22 = add_position_and_value_fields(players_df[players_df['fifa_version'] == 22])

# functions for the lineup visualizations
# original code taken from https://towardsdatascience.com/advanced-sports-visualization-with-pandas-matplotlib-and-seaborn-9c16df80a81b




plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'

formations_dict = {'4-3-1-2': ['GK', 'RB|RWB', 'LCB|CB', 'RCB|CB', 'LB|LWB', 'CDM|CM', 'CDM|CM', 'CDM|CM', 'CAM|CF', 'CF|ST', 'CF|ST'],
                   '4-3-2-1': ['GK', 'RB|RWB', 'LCB|CB', 'RCB|CB', 'LB|LWB', 'CDM|CM', 'CDM|CM', 'CDM|CM', 'CAM|CF', 'CAM|CF', 'CF|ST'],
                   '4-3-3': ['GK', 'RB|RWB', 'LCB|CB', 'RCB|CB', 'LB|LWB', 'CDM|CM', 'CDM|CM', 'CDM|CM', 'RW|RF|ST', 'CF|ST', 'LW|LF|ST'],
                   '4-4-2': ['GK', 'RB|RWB', 'RCB|CB', 'LCB|CB', 'LB|LWB', 'RM|RW', 'CDM|CM', 'CDM|CM', 'LM|LW', 'CF|ST', 'CF|ST'],
                   '4-5-1': ['GK', 'RB|RWB', 'RCB|CB', 'LCB|CB', 'LB|LWB', 'RM|RW', 'CDM|CM', 'CDM|CM', 'LM|LW', 'CF|ST', 'CF|ST'],
                   '3-4-1-2': ['GK', 'RCB|CB', 'CB', 'LCB|CB', 'RM|RW', 'CDM|CM', 'CDM|CM', 'LM|LW', 'CAM|CF', 'CF|ST', 'CF|ST'],
                   '3-4-3': ['GK', 'RCB|CB', 'CB', 'LCB|CB', 'RWB|RM', 'CDM|CM', 'CDM|CM', 'LWB|LM', 'RW|RF|ST', 'CF|ST', 'LW|LF|ST'],
                   '3-5-2': ['GK', 'RCB|CB', 'CB', 'LCB|CB', 'RM|RWB|RB', 'CDM|CM', 'CDM|CM', 'CDM|CM', 'LM|LWB|LB', 'CF|ST', 'CF|ST']}

# dictionary used to calculate the player coordinates on the pitch, based on the number of players per team section such as defence, etc.
xaxis_locations = {1: [40], 2: [30, 50], 3: [25, 40, 55], 4: [10, 30, 50, 70], 5: [10, 25, 40, 55, 70]}


def get_players_section_coord_col(players_coord_dict, players_col_dict, color_val, players_in_section, yaxis_val, team_order):
    if team_order == 'home':
        xaxis_val = xaxis_locations
    elif team_order == 'away':
        xaxis_val = {k: v[::-1] for k, v in xaxis_locations.items()} # reversing the X-axis for the opponent lineup
        yaxis_val = 120 - yaxis_val # total pitch length is 120, so positions have the same distintance from the own team's goal
    else:
        raise ValueError('Invalid team_order value provided - Can be only "home" or "away"')
    for idx, val in enumerate(range(players_in_section)):
        players_coord_dict[len(players_coord_dict)] = [xaxis_val[players_in_section][idx], yaxis_val]
        players_col_dict[len(players_col_dict)] = color_val
    return players_coord_dict, players_col_dict


def get_player_locations_colors(formation, team_type='home'):
    lineup_sections = formation.split('-')
    defenders = int(lineup_sections[0])
    midfielders = int(lineup_sections[1])
    if len(lineup_sections) == 4:
        # trequartista spots are occupied
        trequartistas = int(lineup_sections[2])
        strikers = int(lineup_sections[3])
    elif len(lineup_sections) == 3:
        trequartistas = 0
        strikers = int(lineup_sections[2])
    if len(lineup_sections) not in [3, 4] or (defenders + midfielders + trequartistas + strikers) != 10:
        raise ValueError('Formation invalid - Missing or extra player sections other than defence, midfield, and offence')
    # getting the player locations and colors in two dictionaries that are gradually populated
    locations_dict = {}
    colors_dict = {}
    locations_dict, colors_dict = get_players_section_coord_col(locations_dict, colors_dict, 'darkslategrey', 1, 112, team_type) # GK
    locations_dict, colors_dict = get_players_section_coord_col(locations_dict, colors_dict, 'blue', defenders, 98, team_type) # DEFs
    locations_dict, colors_dict = get_players_section_coord_col(locations_dict, colors_dict, 'gold', midfielders, 84, team_type) # MIDs
    if trequartistas > 0:
        locations_dict, colors_dict = get_players_section_coord_col(locations_dict, colors_dict, 'red', trequartistas, 77, team_type) # CAMs
    locations_dict, colors_dict = get_players_section_coord_col(locations_dict, colors_dict, 'red', strikers, 70, team_type) # STRs
    return locations_dict, colors_dict


def get_best_formation(formation_df, club_name='', measurement='overall'):
    if club_name != '':
        formation_df = formation_df[formation_df['club_name'] == club_name]
    formations_total_vals = {}
    for formation in formations_dict:
        copied_df = formation_df.copy()
        pos_list = formations_dict[formation]
        total_vals = []
        for pos in pos_list:
            # get best record based on 'overall' or 'potential', then drop that record from copied df, so that it cannot be selected again
            if not np.isnan(copied_df[copied_df['best_position'].str.contains(pos)][measurement].max()):
                total_vals.append(copied_df[copied_df['best_position'].str.contains(pos)][measurement].max())
                copied_df.drop(copied_df[copied_df['best_position'].str.contains(pos)][measurement].idxmax(), inplace=True)
        if len(total_vals) == 11:
            formations_total_vals[formation] = sum(total_vals)
        else: # some formations might not find 11 available players - these ones need to be excluded from any possible calcuation
            formations_total_vals[formation] = 0
    best_formation = max(formations_total_vals, key=formations_total_vals.get)
    return best_formation


def get_best_lineup(lineup_df, club_name='', formation='', measurement=''):
    if club_name != '':
        df_copy = lineup_df[lineup_df['club_name'] == club_name]
    else:
        df_copy = lineup_df.copy()
    # if formation is not chosen, then the best one is calculated with a formula
    if formation == '':
        formation = get_best_formation(lineup_df, club_name, measurement)
    squad_lineup = formations_dict[formation]
    squad_default_dict = dict()
    for pos in squad_lineup:
        try:
            best_player_record = df_copy.loc[[df_copy[df_copy['best_position'].str.contains(pos)][measurement].idxmax()]]
        except:
            return formation, 0
        else:
            squad_default_dict[best_player_record['short_name'].to_string(index=False).strip(' \t')] = [
                best_player_record['best_position'].to_string(index=False).strip(' \t'),
                int(best_player_record[measurement].to_string(index=False)),
                int(best_player_record['age'].to_string(index=False)),
                float(best_player_record['value_million_eur'].to_string(index=False)),
                best_player_record['club_name'].to_string(index=False).strip(' \t')]
            df_copy.drop(df_copy[df_copy['best_position'].str.contains(pos)][measurement].idxmax(), inplace=True)
    return formation, squad_default_dict


def draw_pitch(axis):
    # pitch outline and centre line
    pitch = Rectangle([0, 0], width=80, height=120, edgecolor='black', fill=False) # facecolor='#23E04F'
    # left and right penalty area and midline
    left_penalty = Rectangle([22.3, 0], width=35.3, height=14.6, fill=False)
    right_penalty = Rectangle([22.3, 105.4], width=35.3, height=14.6, fill=False)
    midline = ConnectionPatch([0, 60], [80, 60], 'data', 'data')
    # left and right six-yard box
    left_six_yard = Rectangle([32, 0], width=16, height=4.9, fill=False)
    right_six_yard = Rectangle([32, 115.1], width=16, height=4.9, fill=False)
    # prepare circles
    centre_circle = plt.Circle((40, 60), 8.1, color='black', fill=False)
    centre_spot = plt.Circle((40, 60), 0.4, color='black')
    # penalty spots and arcs around penalty boxes
    # left_pen_spot = plt.Circle((40, 9.7), 0.4, color='black')
    # right_pen_spot = plt.Circle((40, 110.3), 0.4, color='black')
    left_arch = Arc((40, 9.5), width=16.2, height=16.2, angle=90, theta1=310, theta2=50, color='black')
    right_arch = Arc((40, 110.4), width=16.2, height=16.2, angle=90, theta1=130, theta2=230, color='black')
    elements_list = [pitch, left_penalty, right_penalty, midline, left_six_yard, right_six_yard, centre_circle, centre_spot,
                     left_arch, right_arch]
    for element in elements_list:
        axis.add_patch(element)


def draw_teams_matchup(home_df, away_df, home_title, away_title, home_team_name='', away_team_name='',
                       home_team_formation='', away_team_formation='', measurement='overall', drawn_pitch='manual'):
    # setting the figure where the matchup will be plotted
    fig = plt.figure()
    fig.set_size_inches(25, 14)
    ax = fig.add_subplot(1, 2, 1)
    if drawn_pitch == 'mplsoccer': # plotting the fancy pitch from 'mplsoccer'
        pitch = VerticalPitch(pitch_color='grass', line_color='white', stripe=True)
        pitch.draw(ax=ax)
    else: # calling the function that draws the pitch
        draw_pitch(ax)
    # setting the field columns shown on the right-hand side of the figure
    if measurement == 'overall':
        note_columns = ('Position', 'Player Name', 'Overall Attribute', 'Age', 'Player Value (in €M)', 'Club Name')
    elif measurement == 'potential':
        note_columns = ('Position', 'Player Name', 'Potential Attribute', 'Age', 'Player Value (in €M)', 'Club Name')
    else:
        raise ValueError('Measurement value provided is not valid (nor "overall" neither "potential")')
    # drawing home team lineup
    home_formation, home_players = get_best_lineup(home_df, home_team_name, home_team_formation, measurement)

    if home_players == 0:
        print("wrong")
        return 1

    home_players_list = list(home_players)
    home_locations_dict, home_colors_dict = get_player_locations_colors(home_formation, team_type='home')
    for i in range(len(home_players_list)):
        player_x, player_y = home_locations_dict[i][0], home_locations_dict[i][1]
        player_color = home_colors_dict[i]
        if '. ' in home_players_list[i]:
            player_name = home_players_list[i].split('. ', 1)[1]
        else:
            player_name = home_players_list[i]
        plt.annotate(player_name,
                     xy = (player_x, player_y), xytext = (0, 18),
                     bbox=dict(boxstyle='round', fc='w'), va='center', ha='center', textcoords='offset points')
        plt.scatter(player_x, player_y, s=250, c=player_color)
    # adding notes on the right-hand side of the home team
    home_team_list = []
    for k, v in home_players.items():
        home_team_list.append([v[0], k, v[1], v[2], v[3], v[4]])
    home_sum_rating = home_sum_age = home_sum_value = 0
    for k, v in home_players.items():
        home_sum_rating = home_sum_rating + v[1]
        home_sum_age = home_sum_age + v[2]
        home_sum_value = home_sum_value + v[3]
    home_notes = [[home_title],
                  ['Average rating: {avg_rating}'.format(avg_rating=round((home_sum_rating/11), 1))],
                  ['Average age: {avg_age}'.format(avg_age=round((home_sum_age/11), 1))],
                  ['Total Value (in €M): {total_value:,}'.format(total_value=round(home_sum_value, 1))]]
    plt_table = plt.table(cellText=home_team_list, colLabels=note_columns,
                          colWidths=[0.3, 0.5, 0.35, 0.2, 0.4, 0.5], cellLoc='right', loc='right', bbox=[1, 0.505, 1.7, 0.36])
    plt_table.scale(1.5, 2)
    for (row, col), cell in plt_table.get_celld().items():
        if (row == 0):
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    plt_home_notes = plt.table(cellText=home_notes, cellLoc='left', loc='left', bbox=[0.9, 0.87, 1.1, 0.12])
    for key, cell in plt_home_notes.get_celld().items():
        cell.set_linewidth(0)
        cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    # drawing away team lineup
    away_formation, away_players = get_best_lineup(away_df, away_team_name, away_team_formation, measurement)

    if away_players == 0:
        print("wrong")
        return 1

    away_players_list = list(away_players)
    away_locations_dict, away_colors_dict = get_player_locations_colors(away_formation, team_type='away')
    for i in range(len(away_players_list)):
        player_x, player_y = away_locations_dict[i][0], away_locations_dict[i][1]
        player_color = away_colors_dict[i]
        if '. ' in away_players_list[i]:
            player_name = away_players_list[i].split('. ', 1)[1]
        else:
            player_name = away_players_list[i]
        plt.annotate(player_name,
                     xy = (player_x, player_y), xytext = (0, 18),
                     bbox=dict(boxstyle='round', fc='w'), va='center', ha='center', textcoords='offset points')
        plt.scatter(player_x, player_y, s=250, c=player_color)
    # adding notes on the right-hand side of the away team
    away_team_list = []
    for k, v in away_players.items():
        away_team_list.append([v[0], k, v[1], v[2], v[3], v[4]])
    away_sum_rating = away_sum_age = away_sum_value = 0
    for k, v in away_players.items():
        away_sum_rating = away_sum_rating + v[1]
        away_sum_age = away_sum_age + v[2]
        away_sum_value = away_sum_value + v[3]
    away_notes = [[away_title],
                  ['Average rating: {avg_rating}'.format(avg_rating=round((away_sum_rating/11), 1))],
                  ['Average age: {avg_age}'.format(avg_age=round((away_sum_age/11), 1))],
                  ['Total Value (in €M): {total_value:,}'.format(total_value=round(away_sum_value, 1))]]
    plt_table = plt.table(cellText=away_team_list, colLabels=note_columns,
                          colWidths=[0.3, 0.5, 0.35, 0.2, 0.4, 0.5], cellLoc='right', loc='right', bbox=[1, 0.015, 1.7, 0.36])
    plt_table.scale(1.5, 2)
    for (row, col), cell in plt_table.get_celld().items():
        if (row == 0):
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    plt_away_notes = plt.table(cellText=away_notes, cellLoc='left', loc='left', bbox=[0.9, 0.38, 1.1, 0.12])
    for key, cell in plt_away_notes.get_celld().items():
        cell.set_linewidth(0)
        cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    # adding the final settings to the plot
    plt.xlim(-2, 82)
    plt.ylim(-2, 122)
    plt.axis('off')
    imgurl = '.\\static\\img\\' + home_title + away_title + '.png'
    plt.savefig(imgurl)
    img = Image.open(imgurl)
    img = img.crop((300, 0, 2400, 1400))
    img.save(imgurl)
    return 0


draw_teams_matchup(df22, df15, 'Dream Team in FIFA 22', 'Dream Team in FIFA 15', home_team_name='FC Barcelona', away_team_name='FC Barcelona', drawn_pitch='mplsoccer')