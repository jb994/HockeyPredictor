#!/usr/bin/env

# V 2.0

### NOTE: Next Step
# I want to make a stat or each team that will be a multiplier
# The stat is CA/GA to see how impactful corsi against a certain team is.
# Hopefully I can use this to modify how likely a team is to score against them based
# On a high CF

#import sys
#sys.path.append('/Users/JackBrons/opt/anaconda2/pkgs')
#from pprint import pprint
#pprint(sys.path)
import math
import numpy as np
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime



print_individual_stats=True

def main():
	### A multiple variable linear regression software used to predict the outcomes of hockey games
	

	#################################################################
	### Please insert the variables below to perform the analysis ###
	#################################################################
	# [['ANA','ARI','BOS','BUF','CAR','CBJ','CGY','CHI','COL','DAL','DET','EDM','FLA','L.A','MIN','MTL','N.J','NSH','NYI','NYR','OTT','PHI','PIT','S.J','STL','T.B','TOR','VAN','VGK','WPG','WSH']]
	home_team="T.B" # From codes above
	away_team="MTL" # From codes above
	day_of_week='Saturday' # [["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]
	todays_date=20191228 #yyyy mmdd
	current_season=2019 #What year did the season start in? (eg. 2018-19 season is 2018)
	do_ref_analysis=False #Not yet a feature
	if do_ref_analysis:
		ref1='name' #First ref's name
		ref2='name' #Second ref's name
		ref_file=open("ref_%s_stats.csv" % (current_season-1))
	else:
		ref_file=None



	team_analysis_w_moneypuck(home_team, away_team, day_of_week, todays_date, current_season)
	
	if ref_file != None:
		ref_file.close()






def team_analysis_w_moneypuck(home_team, away_team, day_of_week, todays_date, current_season):
	home_team_roster_file=open("team_rosters/%s" % (home_team))
	away_team_roster_file=open("team_rosters/%s" % (away_team))

	home_team_xPEN=0
	away_team_xPEN=0

	home_team_xGF=0
	home_team_xGA=0
	home_team_xPPGF=0
	home_team_xSHGA=0
	home_team_xSHGF=0
	home_team_xPPGA=0
	away_team_xGF=0
	away_team_xGA=0
	away_team_xPPGF=0
	away_team_xSHGA=0
	away_team_xSHGF=0
	away_team_xPPGA=0
	
	home_team_roster=home_team_roster_file.readlines()
	away_team_roster=away_team_roster_file.readlines()
	




########################################################################

### Not yet up
	### Predicts home team minor penalties
	print('Starting Home team penalty analysis')
	for index in range(18):
		player=home_team_roster[index].replace("\n",'')
		player_penalties=LinearRegression()
		try:
			stats=pd.read_csv("g2g_stats_moneypuck/%s.csv" % (player))
		except:
			print("No stats for player %s, prediction cannot be made: Aborting" % player)
			quit()

		stats=clean_df(stats, "HOME", day_of_week, todays_date, away_team, current_season)


		stats_all=stats.drop(stats[stats.situation!="all"].index)
		stats_all=stats_all.drop(stats_all[stats_all.season<current_season-2].index)
		AVG_TOI=stats_all['icetime'].sum()/stats_all.shape[0]
		days_since_last_game=str(todays_date-int(stats_all.iloc[[-1]]["gameDate"]))
		player_penalties.fit(stats_all[[away_team, "HOME", 'icetime', day_of_week, "days_since_last_game_"+days_since_last_game]], stats_all['penalties'], sample_weight=stats_all['sample_weight'])
		xPEN = player_penalties.intercept_ + player_penalties.coef_[0] + player_penalties.coef_[1] + AVG_TOI*player_penalties.coef_[2] + player_penalties.coef_[3] + player_penalties.coef_[4]
		if xPEN<0:
			xPEN=0.01
		home_team_xPEN=home_team_xPEN+xPEN
#		print(player + " " + str(xPEN))

	print('')

### Predicts away team minor penalties
	print('Starting Away team penalty analysis')
	for index in range(18):
		player=away_team_roster[index].replace("\n",'')
		player_penalties=LinearRegression()
		try:
			stats=pd.read_csv("g2g_stats_moneypuck/%s.csv" % (player))
		except:
			print("No stats for player %s, prediction cannot be made: Aborting" % player)
			quit()

		stats=clean_df(stats, "AWAY", day_of_week, todays_date, home_team, current_season)


		stats_all=stats.drop(stats[stats.situation!="all"].index)
		stats_all=stats_all.drop(stats_all[stats_all.season<current_season-2].index)
		AVG_TOI=stats_all['icetime'].sum()/stats_all.shape[0]
		days_since_last_game=str(todays_date-int(stats_all.iloc[[-1]]["gameDate"]))
		player_penalties.fit(stats_all[[home_team, "AWAY", 'icetime', day_of_week, "days_since_last_game_"+days_since_last_game]], stats_all['penalties'], sample_weight=stats_all['sample_weight'])
		xPEN = player_penalties.intercept_ + player_penalties.coef_[0] + player_penalties.coef_[1] + AVG_TOI*player_penalties.coef_[2] + player_penalties.coef_[3] + player_penalties.coef_[4]
		if xPEN<0:
			xPEN=0.01
		away_team_xPEN=away_team_xPEN+xPEN
#		print(player + " " + str(xPEN))


	### Calculates Home Team's PP effectiveness
	home_PP_roster_file=open("team_rosters/pp_%s" % home_team)
	for player in home_PP_roster_file.readlines():
		player=player.replace('\n','')
		stats=pd.read_csv("g2g_stats_moneypuck/%s.csv" % (player))
		stats=clean_df(stats, "AWAY", day_of_week, todays_date, away_team, current_season)
		stats_PP=stats.drop(stats[stats.situation!='5on4'].index)
		stats_PP=stats_PP.drop(stats_PP[stats_PP.season<current_season-2].index)
		AVG_TOI=stats_PP['icetime'].sum()/stats_PP.shape[0]
		xTOI=away_team_xPEN*120
		days_since_last_game=str(todays_date-int(stats_PP.iloc[[-1]]["gameDate"]))
		xPPGF,xSHGA=perform_shot_metric_calculations(stats_PP, "HOME", day_of_week, todays_date, away_team, current_season, xTOI)
		home_team_xPPGF=home_team_xPPGF+xPPGF
		home_team_xSHGA=home_team_xSHGA+xSHGA

	### Calculates AWAY Team's PP effectiveness
	away_PP_roster_file=open("team_rosters/pp_%s" % away_team)
	for player in away_PP_roster_file.readlines():
		player=player.replace('\n','')
		stats=pd.read_csv("g2g_stats_moneypuck/%s.csv" % (player))
		stats=clean_df(stats, "HOME", day_of_week, todays_date, home_team, current_season)
		stats_PP=stats.drop(stats[stats.situation!='5on4'].index)
		stats_PP=stats_PP.drop(stats_PP[stats_PP.season<current_season-2].index)
		AVG_TOI=stats_PP['icetime'].sum()/stats_PP.shape[0]
		xTOI=home_team_xPEN*120
		days_since_last_game=str(todays_date-int(stats_PP.iloc[[-1]]["gameDate"]))
		xPPGF,xSHGA=perform_shot_metric_calculations(stats_PP, "AWAY", day_of_week, todays_date, home_team, current_season, xTOI)
		away_team_xPPGF=away_team_xPPGF+xPPGF
		away_team_xSHGA=away_team_xSHGA+xSHGA

	### Calculates Home Team PK effectiveness
	try:
		team_stats=pd.read_csv("team_stats/%s.csv" % (home_team))

	except:
		print("Team stats for %s could not be found: Aborting" % player)
		quit()
	team_all_stats=team_stats.drop(team_stats[team_stats.situation!="all"].index)
	team_all_stats=team_all_stats.drop(team_all_stats[team_all_stats.season<current_season-2].index)
	team_4on5_stats=team_stats.drop(team_stats[team_stats.situation!="4on5"].index)
	team_4on5_stats=team_4on5_stats.drop(team_4on5_stats[team_4on5_stats.season<current_season-2].index)
	total_penalties=float(team_all_stats['penaltiesAgainst'].sum())
	total_PP_goals_against=float(team_4on5_stats['goalsAgainst'].sum())
	home_team_PK_percent=total_PP_goals_against/total_penalties
	xPPGA=home_team_PK_percent*home_team_xPEN
	home_team_xPPGA=xPPGA

	### Calculates AWAY Team PK effectiveness
	try:
		team_stats=pd.read_csv("team_stats/%s.csv" % (away_team))

	except:
		print("Team stats for %s could not be found: Aborting" % away_team)
		quit()
	team_all_stats=team_stats.drop(team_stats[team_stats.situation!="all"].index)
	team_4on5_stats=team_stats.drop(team_stats[team_stats.situation!="4on5"].index)
	total_penalties=float(team_all_stats['penaltiesAgainst'].sum())
	total_PP_goals_against=float(team_4on5_stats['goalsAgainst'].sum())
	away_team_PK_percent=total_PP_goals_against/total_penalties
	xPPGA=away_team_PK_percent*away_team_xPEN
	away_team_xPPGA=xPPGA


##########################################################################
	print("Number of penalties by home team = " + str(home_team_xPEN))
	print("Number of penalties by away team = " + str(away_team_xPEN))

##########################################################################
	print("")


	### Goalie Analysis
	### Returns a list with 3 items: [low_quality_shot_xSV%, medium_quality_shot_xSV%, high_quality_shot_xSV%]
	do_goalie_analysis=True
	try:
		home_goalie_file=open("team_rosters/%s_goalies" % home_team)
		away_goalie_file=open("team_rosters/%s_goalies" % away_team)
		home_goalie=home_goalie_file.readlines()[0].replace('\n','')
		away_goalie=away_goalie_file.readlines()[0].replace('\n','')

	except:
		print("Starting goalie file could not be found, prediction cannot be made: Skipping")
		do_goalie_analysis=False

	if do_goalie_analysis==True:

		try:
			stats=pd.read_csv("g2g_stats_moneypuck/%s.csv" % (home_goalie))
			home_goalie_stats=clean_df(stats, "HOME", day_of_week, todays_date, away_team, current_season)
			home_goalie_stats['highDangerSVP']=home_goalie_stats['highDangerGoals']/home_goalie_stats['highDangerShots']
			home_goalie_stats['mediumDangerSVP']=home_goalie_stats['mediumDangerGoals']/home_goalie_stats['mediumDangerShots']
			home_goalie_stats['lowDangerSVP']=home_goalie_stats['lowDangerGoals']/home_goalie_stats['lowDangerShots']

		except:

			print("No stats for goalie %s, goalie analysis cannot be made: Skipping" % home_goalie)
			do_goalie_analysis=False

	if do_goalie_analysis==True:

		try:
			stats=pd.read_csv("g2g_stats_moneypuck/%s.csv" % (away_goalie))
			away_goalie_stats=clean_df(stats, "AWAY", day_of_week, todays_date, Opp, current_season)
			away_goalie_stats['highDangerSVP']=away_goalie_stats['highDangerGoals']/away_goalie_stats['highDangerShots']
			away_goalie_stats['mediumDangerSVP']=away_goalie_stats['mediumDangerGoals']/away_goalie_stats['mediumDangerShots']
			away_goalie_stats['lowDangerSVP']=away_goalie_stats['lowDangerGoals']/away_goalie_stats['lowDangerShots']

		except:
			print("No stats for player %s, goalie analysis cannot be made: Skipping" % away_goalie)
			do_goalie_analysis=False


	### Returns a list with xSV% of low, medium, and high quality shots
	if do_goalie_analysis==True:
		home_xSVP_list=perform_goalie_analysis(home_goalie_stats, "HOME", day_of_week, todays_date, away_team, current_season)
		away_xSVP_list=perform_goalie_analysis(away_goalie_stats, "AWAY", day_of_week, todays_date, home_team, current_season)


###########################################################################


	### Analysis of Home Team to estimate how many goals for and goals against
	for index in range(18):
		player=home_team_roster[index].replace("\n",'')
		home_team_goal_metrics_list=player_scoring_analysis_moneypuck(player, "HOME", day_of_week, todays_date, away_team, current_season)
		# Returns list in form [xevenGF, xevenGA, xPPGF, xSHGA, xSHGF, xPPGA]
		home_team_xGF=home_team_xGF+home_team_goal_metrics_list[0]
		home_team_xGA=home_team_xGA+home_team_goal_metrics_list[1]
#		home_team_xPPGF=home_team_xPPGF+home_team_goal_metrics_list[2]
#		home_team_xSHGA=home_team_xSHGA+home_team_goal_metrics_list[3]
		home_team_xSHGF=home_team_xSHGF+home_team_goal_metrics_list[4]
#		home_team_xPPGA=home_team_xPPGA+home_team_goal_metrics_list[5]


	#goalie=home_team_roster[18].replace("\n",'')
	#goalie_scoring_analysis_moneypuck()


	print("")


	### Analysis of Away Team to estimate how many goals for and against
	for index in range(18):
		player=away_team_roster[index].replace('\n','')
		away_team_goal_metrics_list=player_scoring_analysis_moneypuck(player, "AWAY", day_of_week, todays_date, home_team, current_season)
		# Returns list in form [xevenGF, xevenGA, xPPGF, xSHGA, xSHGF, xPPGA]
		away_team_xGF=away_team_xGF+away_team_goal_metrics_list[0]
		away_team_xGA=away_team_xGA+away_team_goal_metrics_list[1]
#		away_team_xPPGF=away_team_xPPGF+away_team_goal_metrics_list[2]
#		away_team_xSHGA=away_team_xSHGA+away_team_goal_metrics_list[3]
		away_team_xSHGF=away_team_xSHGF+away_team_goal_metrics_list[4]
#		away_team_xPPGA=away_team_xPPGA+away_team_goal_metrics_list[5]

#		xPPGF, xPPGA=player_special_teams_analysis_moneypuck(player, "AWAY", day_of_week, todays_date, home_team, current_season)


	print("")
	print("Expected Even Strength Goals For Home Team: %s" % (home_team_xGF/5))
	print("Expected Even Strength Goals Against Home Team: %s" % (home_team_xGA/5))
	print("Expected Power Play Goals For Home Team: %s" % (home_team_xPPGF/5))
	print("Expected Short Handed Goals Against Home Team: %s" % (home_team_xSHGA/5))
	print("Expected Short Handed Goals For Home Team: %s" % (home_team_xSHGF/4))
	print("Expected Power Play Goals Against Home Team: %s" % (home_team_xPPGA/4))
	print("Total Expected Goals For Home Team = %s" % (home_team_xGF/5 + home_team_xPPGF/5 + home_team_xSHGF/4))
	print("Total Expected Goals Against Home Team = %s" % (home_team_xGA/5 + home_team_xSHGA/5 + home_team_xPPGA/4))

	print("")
	print("Expected Even Strength Goals For Away Team: %s" % (away_team_xGF/5))
	print("Expected Even Strength Goals Against Away Team: %s" % (away_team_xGA/5))
	print("Expected Power Play Goals For Away Team: %s" % (away_team_xPPGF/5))
	print("Expected Short Handed Goals Against Away Team: %s" % (away_team_xSHGA/5))
	print("Expected Short Handed Goals For Away Team: %s" % (away_team_xSHGF/4))
	print("Expected Power Play Goals Against Away Team: %s" % (away_team_xPPGA/4))
	print("Total Expected Goals For Away Team = %s" % (away_team_xGF/5 + away_team_xPPGF/5 + away_team_xSHGF/4))
	print("Total Expected Goals Against Away Team = %s" % (away_team_xGA/5 + away_team_xSHGA/5 + away_team_xPPGA/4))







def player_scoring_analysis_moneypuck(player, Home_or_Away, Day_of_week, todays_date, Opp, current_season):
	### This analysis takes all the stats from a player and calculate how many expected high, medium, and low quality shots\
	### they will be on the ice for in a game. Variables like whether it is a home or away game, the day of the week, days\
	### since the last game, the player's history against this certain opponent.
	### The shooting percentage for each type of shot is then calculated and an overall stat of how many goals the player\
	### will be on the ice for is calculated.

	### Checks that the player's stat file exists, if not then the program quits
	try:
		stats=pd.read_csv("g2g_stats_moneypuck/%s.csv" % (player))
	except:
		print("No stats for player %s, prediction cannot be made: Aborting" % player)
		quit()

	print(player)
	stats=clean_df(stats, Home_or_Away, Day_of_week, todays_date, Opp, current_season)
	
	
	### Removes stats that are for situations that are not 5on5 or that are over 2 years ago
	stats_5on5=stats.drop(stats[stats.situation!="5on5"].index)
	stats_5on5=stats_5on5.drop(stats_5on5[stats_5on5.season<current_season-2].index)
	stats_5on4=stats.drop(stats[stats.situation!="5on4"].index)
	stats_5on4=stats_5on4.drop(stats_5on4[stats_5on4.season<current_season-2].index)
	stats_4on5=stats.drop(stats[stats.situation!="4on5"].index)
	stats_4on5=stats_4on5.drop(stats_4on5[stats_4on5.season<current_season-2].index)

	#stats_5on5=clean_df(stats_5on5)
	#stats_5on4=clean_df(stats_5on4)
	#stats_4on5=clean_df(stats_4on5)

	#scipy.stats.pearsonr(stats_5on5[''])
	### Adds a variable that contains the day of the week each game was on
	#stats_5on5['day_of_week']=stats_5on5['gameDate'].apply(lambda x: datetime.strptime(str(x),'%Y%m%d').strftime('%A'))

	avg_toi=stats_5on5['icetime'].sum()/stats_5on5.shape[0]
	xevenGF, xevenGA = perform_shot_metric_calculations(stats_5on5, Home_or_Away, Day_of_week, todays_date, Opp, current_season, avg_toi)
	if print_individual_stats==True:
		print("Expected Even Strength Goals For = %s" % (xevenGF))
		print("Expected Even Strength Goals Against = %s" % (xevenGA))
	AVG_TOI=stats_5on4['icetime'].sum()/stats_5on4.shape[0]
	xPPGF, xSHGA = perform_shot_metric_calculations(stats_5on4, Home_or_Away, Day_of_week, todays_date, Opp, current_season, avg_toi)
	if print_individual_stats==True:
		print("Expected PP Goals For = %s" % (xPPGF))
		print("Expected SH Goals Against = %s" % (xSHGA))
	avg_toi=stats_4on5['icetime'].sum()/stats_4on5.shape[0]
	xSHGF, xPPGA = perform_shot_metric_calculations(stats_4on5, Home_or_Away, Day_of_week, todays_date, Opp, current_season, avg_toi)
	if print_individual_stats==True:
		print("Expected SH Goals For = %s" % (xSHGF))
		print("Expected PP Goals Against = %s" % (xPPGA))
	
	return_list= [xevenGF, xevenGA, xPPGF, xSHGA, xSHGF, xPPGA]
	
	return return_list






def perform_shot_metric_calculations(df, Home_or_Away, Day_of_week, todays_date, Opp, current_season, AVG_TOI):


	### This calculates the average time on ice
	
	### Creates the linear regression objects
	mlr_high_danger_for=LinearRegression()
	mlr_medium_danger_for=LinearRegression()
	mlr_low_danger_for=LinearRegression()
	mlr_high_danger_against=LinearRegression()
	mlr_medium_danger_against=LinearRegression()
	mlr_low_danger_against=LinearRegression()

	days_since_last_game=str(todays_date-int(df.iloc[[-1]]["gameDate"]))

	mlr_test1=LinearRegression()
	mlr_test1.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game]], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight'])
	print(mlr_test1.score(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game]], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight']))

	mlr_test=LinearRegression()
	mlr_test.fit(df[[Opp, Home_or_Away, Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight'])
	print(mlr_test.score(df[[Opp, Home_or_Away, Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight']))

	mlr_test=LinearRegression()
	mlr_test.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight'])
	print(mlr_test.score(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight']))

	mlr_test=LinearRegression()
	mlr_test.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'H/A*day_of_week']], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight'])
	print(mlr_test.score(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'H/A*day_of_week']], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight']))

	mlr_test=LinearRegression()
	mlr_test.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'H/A*day_of_week', 'icetime^2']], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight'])
	print(mlr_test.score(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'H/A*day_of_week','icetime^2']], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight']))


	### Creates the prediction system for each type of shot
	mlr_high_danger_for.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight'])
#	print(mlr_high_danger_for.score(df[[Opp, Home_or_Away, 'icetime^2', Day_of_week, "days_since_last_game_"+days_since_last_game]], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight']))
	mlr_medium_danger_for.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['OnIce_F_mediumDangerShots'], sample_weight=df['sample_weight'])
	mlr_low_danger_for.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['OnIce_F_lowDangerShots'], sample_weight=df['sample_weight'])
#	print(mlr_low_danger_for.score(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game]], df['OnIce_F_highDangerShots'], sample_weight=df['sample_weight']))
	mlr_high_danger_against.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['OnIce_A_highDangerShots'], sample_weight=df['sample_weight'])
	mlr_medium_danger_against.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['OnIce_A_mediumDangerShots'], sample_weight=df['sample_weight'])
	mlr_low_danger_against.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['OnIce_A_lowDangerShots'], sample_weight=df['sample_weight'])

	### Calculates how often a high/medium/low quality shot for goes in while this player is on the ice
	high_danger_for_efficiency = float(df['OnIce_F_highDangerGoals'].sum()) / float(df['OnIce_F_highDangerShots'].sum()) if df['OnIce_F_highDangerShots'].sum() else 0
	medium_danger_for_efficiency = float(df['OnIce_F_mediumDangerGoals'].sum()) / float(df['OnIce_F_mediumDangerShots'].sum()) if df['OnIce_F_mediumDangerShots'].sum() else 0
	low_danger_for_efficiency = float(df['OnIce_F_lowDangerGoals'].sum()) / float(df['OnIce_F_lowDangerShots'].sum()) if df['OnIce_F_lowDangerShots'].sum() else 0
	high_danger_against_efficiency = float(df['OnIce_A_highDangerGoals'].sum()) / float(df['OnIce_A_highDangerShots'].sum()) if df['OnIce_A_highDangerShots'].sum() else 0
	medium_danger_against_efficiency = float(df['OnIce_A_mediumDangerGoals'].sum()) / float(df['OnIce_A_mediumDangerShots'].sum()) if df['OnIce_A_mediumDangerShots'].sum() else 0
	low_danger_against_efficiency = float(df['OnIce_A_lowDangerGoals'].sum()) / float(df['OnIce_A_lowDangerShots'].sum()) if df['OnIce_A_lowDangerShots'].sum() else 0

	### Uncomment this section for debugging
#	print(str(mlr_high_danger_for.intercept_)+ ' ' + str(mlr_high_danger_for.coef_[0]) + ' ' + str(mlr_high_danger_for.coef_[1]) + ' ' + str(AVG_TOI*mlr_high_danger_for.coef_[2]) + ' ' + str(mlr_high_danger_for.coef_[3]) + ' ' + str(mlr_high_danger_for.coef_[4]))
#	print(str(mlr_medium_danger_for.intercept_) + ' ' + str(mlr_medium_danger_for.coef_[0]) + ' ' + str(mlr_medium_danger_for.coef_[1]) + ' ' + str(AVG_TOI*mlr_medium_danger_for.coef_[2]) + ' ' + str(mlr_medium_danger_for.coef_[3]) + ' ' + str(mlr_medium_danger_for.coef_[4]))
#	print(str(mlr_low_danger_for.intercept_) + ' ' + str(mlr_low_danger_for.coef_[0]) + ' ' + str(mlr_low_danger_for.coef_[1]) + ' ' + str(AVG_TOI*mlr_low_danger_for.coef_[2]) + ' ' + str(mlr_low_danger_for.coef_[3]) + ' ' + str(mlr_low_danger_for.coef_[4]))
#	print(str(mlr_high_danger_against.intercept_) + ' ' + str(mlr_high_danger_against.coef_[0]) + ' ' + str(mlr_high_danger_against.coef_[1]) + ' ' + str(AVG_TOI*mlr_high_danger_against.coef_[2]) + ' ' + str(mlr_high_danger_against.coef_[3]) + ' ' + str(mlr_high_danger_against.coef_[4]))
#	print(str(mlr_medium_danger_against.intercept_) + ' ' + str(mlr_medium_danger_against.coef_[0]) + ' ' + str(mlr_medium_danger_against.coef_[1]) + ' ' + str(AVG_TOI*mlr_medium_danger_against.coef_[2]) + ' ' + str(mlr_medium_danger_against.coef_[3]) + ' ' + str(mlr_medium_danger_against.coef_[4]))
#	print(str(mlr_low_danger_against.intercept_ )+ ' ' + str(mlr_low_danger_against.coef_[0]) + ' ' + str(mlr_low_danger_against.coef_[1]) + ' ' + str(AVG_TOI*mlr_low_danger_against.coef_[2]) + ' ' + str(mlr_low_danger_against.coef_[3]) + ' ' + str(mlr_low_danger_against.coef_[4]))

	### Does the actual calculation for expected high/medium/low shots for/against the player's team while he is on the ice
	xHDF = mlr_high_danger_for.intercept_ + mlr_high_danger_for.coef_[0] + mlr_high_danger_for.coef_[1] + AVG_TOI*mlr_high_danger_for.coef_[2] + mlr_high_danger_for.coef_[3] + mlr_high_danger_for.coef_[4] + mlr_high_danger_for.coef_[5]*(AVG_TOI**2)
#	print(mlr_high_danger_for.coef_[0])
#	print(mlr_high_danger_for.coef_[1])
#	print(mlr_high_danger_for.coef_[2])
#	print(mlr_high_danger_for.coef_[3])
#	print(mlr_high_danger_for.coef_[4])
	xMDF = mlr_medium_danger_for.intercept_ + mlr_medium_danger_for.coef_[0] + mlr_medium_danger_for.coef_[1] + AVG_TOI*mlr_medium_danger_for.coef_[2] + mlr_medium_danger_for.coef_[3] + mlr_medium_danger_for.coef_[4]+ mlr_medium_danger_for.coef_[5]*(AVG_TOI**2)
	xLDF = mlr_low_danger_for.intercept_ + mlr_low_danger_for.coef_[0] + mlr_low_danger_for.coef_[1] + AVG_TOI*mlr_low_danger_for.coef_[2] + mlr_low_danger_for.coef_[3] + mlr_low_danger_for.coef_[4]+ mlr_low_danger_for.coef_[5]*(AVG_TOI**2)
	xHDA = mlr_high_danger_against.intercept_ + mlr_high_danger_against.coef_[0] + mlr_high_danger_against.coef_[1] + AVG_TOI*mlr_high_danger_against.coef_[2] + mlr_high_danger_against.coef_[3] + mlr_high_danger_against.coef_[4]+ mlr_high_danger_against.coef_[5]*(AVG_TOI**2)
	xMDA = mlr_medium_danger_against.intercept_ + mlr_medium_danger_against.coef_[0] + mlr_medium_danger_against.coef_[1] + AVG_TOI*mlr_medium_danger_against.coef_[2] + mlr_medium_danger_against.coef_[3] + mlr_medium_danger_against.coef_[4]+ mlr_medium_danger_against.coef_[5]*(AVG_TOI**2)
	xLDA = mlr_low_danger_against.intercept_ + mlr_low_danger_against.coef_[0] + mlr_low_danger_against.coef_[1] + AVG_TOI*mlr_low_danger_against.coef_[2] + mlr_low_danger_against.coef_[3] + mlr_low_danger_against.coef_[4]+ mlr_low_danger_against.coef_[5]*(AVG_TOI**2)
	
	### This part calculates how many goals for and against the player will be on for
	#print("xGF= %s*%s + %s*%s + %s*%s" % (xHDF, high_danger_for_efficiency, xMDF, medium_danger_for_efficiency, xLDF, low_danger_for_efficiency))
	xGF= xHDF*high_danger_for_efficiency + xMDF*medium_danger_for_efficiency + xLDF*low_danger_for_efficiency
	xGA= xHDA*high_danger_against_efficiency + xMDA*medium_danger_against_efficiency + xLDA*low_danger_against_efficiency
	
	### Uncomment to print the specific expected goals for and against for this player
	#print(player)

	if xGF<0:
		xGF=0
	if xGA<0:
		xGA=0
	xGF, xGA

	return xGF, xGA


def clean_df(df, Home_or_Away, Day_of_week, todays_date, Opp, current_season):

	new_df=df
	new_df.sort_values(by = 'gameDate', inplace= True)
	new_df['day_of_week']=new_df['gameDate'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d').strftime('%A'))
	

	new_df=pd.get_dummies(new_df, columns=['home_or_away'], prefix='', prefix_sep='')
	new_df=pd.get_dummies(new_df, columns=['opposingTeam'], prefix='', prefix_sep='')
	new_df=pd.get_dummies(new_df, columns=['day_of_week'], prefix='', prefix_sep='')

	days_between_games_list=count_days_between_games_moneypuck(new_df['gameDate'])
	new_df['days_since_last_game']=days_between_games_list
	new_df=pd.get_dummies(new_df, columns=['days_since_last_game'], prefix=None)

	### This part creates a new column specifying how much the program should weight each game's data
	### based on how long ago the game was
	k=1 #Scaling-Constant
	T=1587 #Time-Constant #1587
#	new_df['sample_weight']=new_df['gameDate'].apply(lambda x: k*math.exp(-(todays_date-int(x))/T))
	new_df['sample_weight']=new_df['gameDate'].apply(lambda x: 1)
#	new_df['sample_weight']=new_df['gameDate'].apply(lambda x: determine_sample_weight(x))

	new_df['icetime^2']=new_df['icetime'].apply(lambda x: x**2)
	### If a player has never been in a certain situation (eg. never played game on wednesday) then variable is set to 0 for all rows
	if Opp not in new_df.columns:
		new_df[Opp]=np.zeros(new_df.shape[0], dtype=int)
	if Home_or_Away not in new_df.columns:
		new_df[Home_or_Away]=np.zeros(new_df.shape[0], dtype=int)
	if Day_of_week not in new_df.columns:
		new_df[Day_of_week]=np.zeros(new_df.shape[0], dtype=int)
	days_since_last_game=str(todays_date-int(new_df.iloc[[-1]]["gameDate"]))
	if (int(days_since_last_game)<1):
		print("Incorrect input for game date: Aborting")
		quit()
	if "days_since_last_game_"+days_since_last_game not in new_df.columns:
		new_df["days_since_last_game_"+days_since_last_game]=np.zeros(new_df.shape[0], dtype=int)

	new_df['H/A*day_of_week']=new_df[Home_or_Away]*new_df[Day_of_week]
	

	return new_df



def player_PP_analysis_moneypuck(df, Home_or_Away, Day_of_week, todays_date, Opp, current_season, xPPs):
	percent_of_team_PP_time=df['icetime'].sum()/(df['timeOnBench'].sum() + df['icetime'].sum())

	mlr_high_danger_for=LinearRegression()
	mlr_medium_danger_for=LinearRegression()
	mlr_low_danger_for=LinearRegression()
	mlr_high_danger_against=LinearRegression()
	mlr_medium_danger_against=LinearRegression()
	mlr_low_danger_against=LinearRegression()

	if Opp not in df.columns:
		df[Opp]=np.zeros(df.shape[0], dtype=int)
	if Home_or_Away not in df.columns:
		df[Home_or_Away]=np.zeros(df.shape[0], dtype=int)
	if Day_of_week not in df.columns:
		df[Day_of_week]=np.zeros(df.shape[0], dtype=int)
	if "days_since_last_game_"+days_since_last_game not in df.columns:
		df["days_since_last_game_"+days_since_last_game]=np.zeros(df.shape[0], dtype=int)







def perform_goalie_analysis(df, Home_or_Away, day_of_week, todays_date, opp, current_season):
	mlr_high_danger_xshots=LinearRegression()
	mlr_medium_danger_xshots=LinearRegression()
	mlr_low_danger_xshots=LinearRegression()
	mlr_high_danger_shot_xsave_percentage=LinearRegression()
	mlr_medium_danger_shot_xsave_percentage=LinearRegression()
	mlr_low_danger_shot_xsave_percentage=LinearRegression()

	mlr_high_danger_xshots.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['highDangerShots'], sample_weight=df['sample_weight'])
	mlr_medium_danger_xshots.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['mediumDangerShots'], sample_weight=df['sample_weight'])
	mlr_low_danger_xshots.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['lowDangerShots'], sample_weight=df['sample_weight'])
	mlr_high_danger_shot_xsave_percentage.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['highDangerSVP'], sample_weight=df['sample_weight'])
	mlr_medium_danger_shot_xsave_percentage.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['mediumDangerSVP'], sample_weight=df['sample_weight'])
	mlr_low_danger_shot_xsave_percentage.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game, 'icetime^2']], df['lowDangerSVP'], sample_weight=df['sample_weight'])

	return None


def player_even_strength_analysis_moneypuck():
	None

def player_PK_analysis_moneypuck():
	None
	






def count_days_between_games_moneypuck(dates_list):
	# This Function calculates and records the number of days since the last game
	# If the number is greater than 6, then it is recorded as 7
	# The most recent game gets a score of 0
	days_between_games_list=[]
	i=0
	for index, date in dates_list.iteritems():
		item=str(date)
		if i==0:
			days_between_games_list.append(7)
			previous_item=item
			i=1
		else:
			# Calculates date of most recent game minus date of last game
			number_of_days_since_last_game=(datetime.strptime(item,"%Y%m%d") - datetime.strptime(previous_item,"%Y%m%d")).days
			if number_of_days_since_last_game==0:
				days_between_games_list.append(days_between_games_list[-1])
			elif number_of_days_since_last_game<=7:
				days_between_games_list.append(number_of_days_since_last_game)
			elif number_of_days_since_last_game>7:
				days_between_games_list.append(7)
			#days_between_games_list.append(number_of_days_since_last_game)
			if days_between_games_list[-1]<0:
				print("Note: error in dataset. There are repeated games in player's stats")
				print(days_between_games_list)
				print(dates_list)

			previous_item=item
			
	#print(days_between_games_list)
	#print("Len of list = %s" % (len(days_between_games_list)))
	return days_between_games_list






main()