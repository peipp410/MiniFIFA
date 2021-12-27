from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.http import Http404
import numpy as np
import matplotlib.pyplot as plt
import pickle
import display
import playerDraw


def home_view(request):
    return render(request, "index.html")


def team_view(request):
    teams = {}
    tname = '%'
    pname = '%'
    url = ['']
    if request.POST:
        queryRes = []
        tname += request.POST['teamname']
        tname += '%'
        pname += request.POST['playername']
        pname += '%'
        with connection.cursor() as cursor:
            query = '''
            select ID, `Name`, Age, Height, Weight, Nationality, Positions, Club, ClubJoined
            from footballmodel_player natural join footballmodel_playerbasic natural join footballmodel_playerclub
            where Club like %s and `Name` like %s;
            '''
            cursor.execute(query, [tname, pname])
            resp = cursor.fetchall()
            i = 1
            for rows in resp:
                ls = list(rows)
                queryRes.append(ls)
                teams[i] = {
                    'ID': ls[0],
                    'Name': ls[1],
                    'Age': ls[2],
                    'Height': ls[3],
                    'Weight': ls[4],
                    'Nationality': ls[5],
                    'Positions': ls[6],
                    'Club': ls[7],
                    'ClubJoined': ls[8]
                }
                i += 1
            if i == 2:
                query2 = '''
                select PhotoUrl
                from footballmodel_player natural join footballmodel_playerphoto
                where `Name` = %s;
                '''
                cursor.execute(query2, [ls[1]])
                resp2 = cursor.fetchone()
                url = list(resp2)
    # if request.is_ajax():
    #     if request.GET.get('export') == 'yes':
    #         print(queryRes)
    #     else:
    #         raise Http404
    return render(request, "team.html", {'teams': teams})


def draw(arr):
    mult = 1
    for i in range(len(arr)):
        mult *= arr[i]
    arr = arr/100
    feature = np.array(['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical'])
    plt.clf()
    plt.rcParams['axes.unicode_minus'] = False
    plt.style.use('seaborn-paper')
    angles = np.linspace(0.3 * np.pi, 2.3 * np.pi, len(feature), endpoint=False)
    values = np.concatenate((arr, [arr[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    feature = np.concatenate((feature, [feature[0]]))
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(angles * 180 / np.pi, feature)
    ax.tick_params(labelsize=15)
    ax.set_ylim(0, 1)
    ax.grid(True)
    ax.tick_params('y', labelleft=False)
    plt.savefig('.\\static\\img\\'+str(int(mult))+'.png')
    return int(mult)


def evaluation_view(request):
    attr = np.zeros(6)
    radaratt = 'Here is the radar plot for the 6 skills of this player.'
    imgurl = ''
    result = 'The overall score for the skills of this player is %.2f. '
    eval = {}
    if request.POST:
        attr[0] = int(request.POST['pace'])
        attr[1] = int(request.POST['shooting'])
        attr[2] = int(request.POST['passing'])
        attr[3] = int(request.POST['dribbling'])
        attr[4] = int(request.POST['defending'])
        attr[5] = int(request.POST['physical'])
        imgno = draw(attr)
        imgurl = '.\\static\\img\\'+str(int(imgno))+'.png'
        eval['radar'] = imgurl
        eval['radaratt'] = radaratt

        vector = np.zeros((1, 6))
        vector[0] = attr
        with open('./predict_Overall.pickle', 'rb') as f:
            clf_Overall = pickle.load(f)
            preOverall = clf_Overall.predict(vector)[0]
            result = result % preOverall
        with open('./predict_Potential.pickle', 'rb') as f:
            clf_Potential = pickle.load(f)
            prePotential = clf_Potential.predict(vector)[0]
            if prePotential == 1:
                result += 'This player is full of potential. Hope he can train hard and achieve better results.'
            else:
                result += 'Oh, oops! It seems that this player has poor skills and he has to train harder to achieve good results!'
            eval['result'] = result
        players = {}
        with connection.cursor() as cursor:
            query = '''
            select ID, `Name`, Club, Overall
            from footballmodel_player natural join footballmodel_playerbasic natural join footballmodel_playermodel
            where abs(%s - Overall) <= 2
            limit 5;
            '''
            cursor.execute(query, [int(preOverall)])
            resp = cursor.fetchall()
            i = 1
            for rows in resp:
                ls = list(rows)
                players[i] = {
                    'ID': ls[0],
                    'Name': ls[1],
                    'Club': ls[2],
                    'Overall': ls[3]
                }
                i += 1
        eval['players'] = players
    return render(request, "evaluation.html", eval)


def players(request, playerID):
    ID = int(playerID)
    player = {}
    total_attr = ['ID', 'Crossing', 'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling', 'Curve',
                  'FKAccuracy', 'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions',
                  'Balance', 'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions',
                  'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle', 'SlidingTackle',
                  'GKDiving', 'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes']
    with connection.cursor() as cursor:
        query1 = '''
        select ID, FullName, Age, Height, Weight, Positions, ClubPosition, Nationality, ValueEUR, Club, NationalTeam, 
            PreferredFoot, WageEUR, AttackingWorkRate, DefensiveWorkRate, PhotoUrl 
        from footballmodel_player natural join footballmodel_playerbasic 
            natural join footballmodel_playerdetail natural join footballmodel_playerphoto
        where ID = %s;
        '''
        cursor.execute(query1, [ID])
        resp = cursor.fetchone()
        ls = list(resp)
        player['ID'] = ls[0]
        player['FullName'] = ls[1]
        player['Age'] = ls[2]
        player['Height'] = ls[3]
        player['Weight'] = ls[4]
        player['Positions'] = ls[5]
        player['ClubPosition'] = ls[6]
        player['Nationality'] = ls[7]
        player['ValueEUR'] = ls[8]
        player['Club'] = ls[9]
        player['NationalTeam'] = ls[10]
        player['PreferredFoot'] = ls[11]
        player['WageEUR'] = ls[12]
        player['AttackingWorkRate'] = ls[13]
        player['DefensiveWorkRate'] = ls[14]
        player['playerimg'] = ls[15]

        query2 = '''
        select * from footballmodel_playerdisplay where ID = %s
        '''
        cursor.execute(query2, [ID])
        total = cursor.fetchone()
        total = list(total)
        attacking = total[1:6]
        att_attr = total_attr[1:6]
        playerDraw.draw_radar(np.array(attacking), np.array(att_attr), "attacking")
        skill = total[6:11]
        skill_attr = total_attr[6:11]
        playerDraw.draw_radar(np.array(skill), np.array(skill_attr), "skill")
        movement = total[11:16]
        movement_attr = total_attr[11:16]
        playerDraw.draw_radar(np.array(movement), np.array(movement_attr), "movement")
        power = total[16:21]
        power_attr = total_attr[16:21]
        playerDraw.draw_radar(np.array(power), np.array(power_attr), "power")
        mentality = total[21:26]
        mentality_attr = total_attr[21:26]
        playerDraw.draw_radar(np.array(mentality), np.array(mentality_attr), "mentality")

        query3 = '''
        select * from footballmodel_playerrating where ID = %s;
        '''
        cursor.execute(query3, [ID])
        rating = cursor.fetchone()
        rating = list(rating)
        playerDraw.draw_rating(rating[1:])

    return render(request, "playerProfile.html", player)


def management_view(request):
    year1 = ''
    year2 = ''
    name1 = ''
    name2 = ''
    club1 = ''
    club2 = ''
    formation1 = ''
    formation2 = ''
    imgurl = ''
    indicator = 0
    if request.POST:
        year1 += request.POST['year1']
        year2 += request.POST['year2']
        name1 += request.POST['name1']
        name2 += request.POST['name2']
        club1 += request.POST['club1']
        club2 += request.POST['club2']
        formation1 += request.POST['formation1']
        formation2 += request.POST['formation2']
        if name1 != '' and name2 != '':
            def get_df(num):
                years = {
                    '2015': display.df15,
                    '2016': display.df16,
                    '2017': display.df17,
                    '2018': display.df18,
                    '2019': display.df19,
                    '2020': display.df20,
                    '2021': display.df21,
                    '2022': display.df22
                }
                return years.get(num, None)
            df1 = get_df(year1)
            df2 = get_df(year2)

            indicator = display.draw_teams_matchup(df1, df2, name1, name2, club1, club2, formation1, formation2, drawn_pitch='mplsoccer')

            if indicator == 0:
                imgurl = '.\\static\\img\\' + name1 + name2 + '.png'
            else:
                imgurl = '.\\static\\img\\404.jpg'
    return render(request, "management.html", {'manage': imgurl, 'indicator': indicator})


def clubs(request, clubname):
    name = clubname
    clubrender = {}
    with connection.cursor() as cursor:
        query = '''
        select Club, League, TransferBudget, DomesticPrestige, IntPrestige, Players, StartingAverageAge, 
        AllTeamAverageAge, Overall, Attack, Midfield, Defence, club_logo_url
        from footballmodel_clubphoto natural join footballmodel_clubbasic
        where Club = %s;
        '''
        cursor.execute(query, [name])
        clubinfo = cursor.fetchone()
        clubinfo = list(clubinfo)
        clubrender['Name'] = clubinfo[0]
        clubrender['League'] = clubinfo[1]
        clubrender['TransferBudget'] = clubinfo[2]
        clubrender['DomesticPrestige'] = clubinfo[3]
        clubrender['IntPrestige'] = clubinfo[4]
        clubrender['Players'] = clubinfo[5]
        clubrender['StartingAverageAge'] = clubinfo[6]
        clubrender['AllTeamAverageAge'] = clubinfo[7]
        clubrender['Overall'] = clubinfo[8]
        clubrender['Attack'] = clubinfo[9]
        clubrender['Midfield'] = clubinfo[10]
        clubrender['Defence'] = clubinfo[11]
        clubrender['cluburl'] = clubinfo[12]

    return render(request, "teamProfile.html", clubrender)


def about_view(request):
    return render(request, "about.html")


def tutorial_view(request):
    return render(request, "tutorial.html")
