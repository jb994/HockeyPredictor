#!/usr/bin/env

# V 1.0

### NOTE: Next Step
# I want to make a stat or each team that will be a multiplier
# The stat is CA/GA to see how impactful corsi against a certain team is.
# Hopefully I can use this to modify how likely a team is to score against them based
# On a high CF

#import sys
#sys.path.append('/Users/JackBrons/opt/anaconda2/pkgs')
#from pprint import pprint
#pprint(sys.path)
import os
import numpy as np
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, date



print_individual_stats=False # Prints the individual predicted stats for each player
calculate_penalties=False # Unavailable
do_goalie_analysis=False # Will perform an additional goalie stat analysis at the end
allow_past_analysis=True # Let's the user put in game's from a past date, assuming the correct roster is used

def main(game_info_list):
	### A multiple variable linear regression software used to predict the outcomes of hockey games
	

	#################################################################
	### Please insert the variables below to perform the analysis ###
	#################################################################
	# [['ANA','ARI','BOS','BUF','CAR','CBJ','CGY','CHI','COL','DAL','DET','EDM','FLA','L.A','MIN','MTL','N.J','NSH','NYI','NYR','OTT','PHI','PIT','S.J','STL','T.B','TOR','VAN','VGK','WPG','WSH']]
	home_team=game_info_list[2] # From codes above
	away_team=game_info_list[3] # From codes above

	weekDays=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	year=int(game_info_list[1][0]+game_info_list[1][1]+game_info_list[1][2]+game_info_list[1][3])
	month=int(game_info_list[1][4]+game_info_list[1][5])
	day=int(game_info_list[1][6]+game_info_list[1][7])
	day_of_week=weekDays[date(year,month,day).weekday()]
#	day_of_week='Saturday' # [["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]
	todays_date=int(game_info_list[1]) #yyyymmdd
	current_season=int(game_info_list[0][0:4]) #What year did the season start in (eg. 2018-19 season is 2018)
	do_ref_analysis=False #Not yet a feature
	if do_ref_analysis:
		ref1='name' #First ref's name
		ref2='name' #Second ref's name
		ref_file=open("ref_%s_stats.csv" % (current_season))
	else:
		ref_file=None



	return_list=team_analysis_w_moneypuck(home_team, away_team, day_of_week, todays_date, current_season, game_info_list[5:23], game_info_list[23:41])
	
	if ref_file != None:
		ref_file.close()

	###	returns [home_team_xGF/5, home_team_xGA/5, home_team_xGF/5 + home_team_xPPGF/5 + home_team_xSHGF/4, home_team_xGA/5 + home_team_xSHGA/5 + home_team_xPPGA/4, away_team_xGF/5, away_team_xGA/5, away_team_xGF/5 + away_team_xPPGF/5 + away_team_xSHGF/4, away_team_xGA/5 + away_team_xSHGA/5 + away_team_xPPGA/4]
	### [home_team_xGF, home_team_xGA, home_team_xGF_all_sit, home_team_xGA_all_sit, away_team_xGF, away_team_xGA, away_team_xGF_all_sit, away_team_xGA_all_sit]
	return return_list




def team_analysis_w_moneypuck(home_team, away_team, day_of_week, todays_date, current_season, home_team_roster, away_team_roster):
	### This function predicts how many goals each team is supposed to score and let in by \
	### using regression analysis to determine how many high, medium, and low scoring chances\
	### each player will get and how many they will capitalize on.
#	home_team_roster_file=open("team_rosters/%s" % (home_team))
#	away_team_roster_file=open("team_rosters/%s" % (away_team))

	### Initializes all the variables used to record predicted stats
	home_team_xPEN=0
	away_team_xPEN=0

	home_team_xGF=0
	home_team_xGA=0
	home_team_xPPGF=0
	home_team_xSHGA=0
	home_team_xSHGF=0
	home_team_xPPGA=0
	home_team_xHDA=0
	home_team_xMDA=0
	home_team_xLDA=0
	away_team_xGF=0
	away_team_xGA=0
	away_team_xPPGF=0
	away_team_xSHGA=0
	away_team_xSHGF=0
	away_team_xPPGA=0
	away_team_xHDA=0
	away_team_xMDA=0
	away_team_xLDA=0

	
#	home_team_roster=home_team_roster_file.readlines()
#	away_team_roster=away_team_roster_file.readlines()
	




########################################################################
	if calculate_penalties==True:
	### Not yet up
		### Predicts home team minor penalties
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
			AVG_TOI=stats_all['icetime'].sum()/stats_all.shape[0]
			days_since_last_game=str(todays_date-int(stats_all.iloc[[-1]]["gameDate"]))
			player_penalties.fit(stats_all[[away_team, "HOME", 'icetime', day_of_week, "days_since_last_game_"+days_since_last_game]], stats_all['penalties'])

			if stats_all[away_team].sum() == 0:
				Opp_coef=0
			else:
				Opp_coef=1
			if stats_all["HOME"].sum() == 0:
				H_A_coef=0
			else:
				H_A_coef=1
			if stats_all[day_of_week].sum() == 0:
				DOW_coef=0
			else:
				DOW_coef=1	

			xPEN = player_penalties.intercept_ + Opp_coef*player_penalties.coef_[0] + H_A_coef*player_penalties.coef_[1] + AVG_TOI*player_penalties.coef_[2] + DOW_coef*player_penalties.coef_[3] + player_penalties.coef_[4]
			if xPEN<0:
				xPEN=0.01
			home_team_xPEN=home_team_xPEN+xPEN
	#		print(player + " " + str(xPEN))

	### Predicts away team minor penalties
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
			AVG_TOI=stats_all['icetime'].sum()/stats_all.shape[0]
			days_since_last_game=str(todays_date-int(stats_all.iloc[[-1]]["gameDate"]))
			player_penalties.fit(stats_all[[home_team, "AWAY", 'icetime', day_of_week, "days_since_last_game_"+days_since_last_game]], stats_all['penalties'])

			if stats_all[home_team].sum() == 0:
				Opp_coef=0
			else:
				Opp_coef=1
			if stats_all["AWAY"].sum() == 0:
				H_A_coef=0
			else:
				H_A_coef=1
			if stats_all[day_of_week].sum() == 0:
				DOW_coef=0
			else:
				DOW_coef=1	

			xPEN = player_penalties.intercept_ + Opp_coef*player_penalties.coef_[0] + H_A_coef*player_penalties.coef_[1] + AVG_TOI*player_penalties.coef_[2] + DOW_coef*player_penalties.coef_[3] + player_penalties.coef_[4]
			if xPEN<0:
				xPEN=0.01
			away_team_xPEN=away_team_xPEN+xPEN
	#		print(player + " " + str(xPEN))

	##########################################################################
		print("Number of penalties by home team = " + str(home_team_xPEN))
		print("Number of penalties by away team = " + str(away_team_xPEN))


		print("")


	### Analysis of Home Team to estimate how many goals for and goals against
	for index in range(18):
		player=home_team_roster[index].replace("\n",'')
#		print(player)
		home_team_goal_metrics_list=player_scoring_analysis_moneypuck(player, "HOME", day_of_week, todays_date, away_team, current_season)
		if type(home_team_goal_metrics_list)==bool:
			return False
		# Returns list in form [xevenGF, xevenGA, xPPGF, xSHGA, xSHGF, xPPGA]
		home_team_xGF=home_team_xGF+home_team_goal_metrics_list[0]
		home_team_xGA=home_team_xGA+home_team_goal_metrics_list[1]
		home_team_xPPGF=home_team_xPPGF+home_team_goal_metrics_list[2]
		home_team_xSHGA=home_team_xSHGA+home_team_goal_metrics_list[3]
		home_team_xSHGF=home_team_xSHGF+home_team_goal_metrics_list[4]
		home_team_xPPGA=home_team_xPPGA+home_team_goal_metrics_list[5]
		home_team_xHDA=home_team_xHDA+home_team_goal_metrics_list[6]
		home_team_xMDA=home_team_xMDA+home_team_goal_metrics_list[7]
		home_team_xLDA=home_team_xLDA+home_team_goal_metrics_list[8]


	#goalie=home_team_roster[18].replace("\n",'')
	#goalie_scoring_analysis_moneypuck()


	print("")


	### Analysis of Away Team to estimate how many goals for and against
	for index in range(18):
		player=away_team_roster[index].replace('\n','')
#		print(player)
		away_team_goal_metrics_list=player_scoring_analysis_moneypuck(player, "AWAY", day_of_week, todays_date, home_team, current_season)
		if type(away_team_goal_metrics_list)==bool:
			return False
		# Returns list in form [xevenGF, xevenGA, xPPGF, xSHGA, xSHGF, xPPGA]
		away_team_xGF=away_team_xGF+away_team_goal_metrics_list[0]
		away_team_xGA=away_team_xGA+away_team_goal_metrics_list[1]
		away_team_xPPGF=away_team_xPPGF+away_team_goal_metrics_list[2]
		away_team_xSHGA=away_team_xSHGA+away_team_goal_metrics_list[3]
		away_team_xSHGF=away_team_xSHGF+away_team_goal_metrics_list[4]
		away_team_xPPGA=away_team_xPPGA+away_team_goal_metrics_list[5]
		away_team_xHDA=away_team_xHDA+away_team_goal_metrics_list[6]
		away_team_xMDA=away_team_xMDA+away_team_goal_metrics_list[7]
		away_team_xLDA=away_team_xLDA+away_team_goal_metrics_list[8]

#		xPPGF, xPPGA=player_special_teams_analysis_moneypuck(player, "AWAY", day_of_week, todays_date, home_team, current_season)




#	print("")
#	print("Expected Even Strength Goals For Home Team: %s" % (home_team_xGF/5))
#	print("Expected Even Strength Goals Against Home Team: %s" % (home_team_xGA/5))
#	print("Expected Power Play Goals For Home Team: %s" % (home_team_xPPGF/5))
#	print("Expected Short Handed Goals Against Home Team: %s" % (home_team_xSHGA/5))
#	print("Expected Short Handed Goals For Home Team: %s" % (home_team_xSHGF/4))
#	print("Expected Power Play Goals Against Home Team: %s" % (home_team_xPPGA/4))
#	print("Total Expected Goals For Home Team = %s" % (home_team_xGF/5 + home_team_xPPGF/5 + home_team_xSHGF/4))
#	print("Total Expected Goals Against Home Team = %s" % (home_team_xGA/5 + home_team_xSHGA/5 + home_team_xPPGA/4))

#	print("")
#	print("Expected Even Strength Goals For Away Team: %s" % (away_team_xGF/5))
#	print("Expected Even Strength Goals Against Away Team: %s" % (away_team_xGA/5))
#	print("Expected Power Play Goals For Away Team: %s" % (away_team_xPPGF/5))
#	print("Expected Short Handed Goals Against Away Team: %s" % (away_team_xSHGA/5))
#	print("Expected Short Handed Goals For Away Team: %s" % (away_team_xSHGF/4))
#	print("Expected Power Play Goals Against Away Team: %s" % (away_team_xPPGA/4))
#	print("Total Expected Goals For Away Team = %s" % (away_team_xGF/5 + away_team_xPPGF/5 + away_team_xSHGF/4))
#	print("Total Expected Goals Against Away Team = %s" % (away_team_xGA/5 + away_team_xSHGA/5 + away_team_xPPGA/4))

	return [home_team_xGF/5, home_team_xGA/5, home_team_xGF/5 + home_team_xPPGF/5 + home_team_xSHGF/4, home_team_xGA/5 + home_team_xSHGA/5 + home_team_xPPGA/4, away_team_xGF/5, away_team_xGA/5, away_team_xGF/5 + away_team_xPPGF/5 + away_team_xSHGF/4, away_team_xGA/5 + away_team_xSHGA/5 + away_team_xPPGA/4]

	if do_goalie_analysis==True:
		print("")
		if len(home_team_roster)!=19 or len(away_team_roster)!=19:
			print("Goalie analysis cannot be conducted because name of goalie is missing")
		else:
			home_goalie=home_team_roster[18].replace("\n",'')
			away_goalie=away_team_roster[18].replace("\n",'')
			if os.path.isfile(('g2g_stats_moneypuck/%s.csv') % home_goalie):
				home_goalie_stats=pd.read_csv("g2g_stats_moneypuck/%s.csv" % (home_goalie))
				home_goalie_stats=clean_df(home_goalie_stats, "HOME", day_of_week, todays_date, away_team, current_season)
				home_goalie_stats=home_goalie_stats.drop(home_goalie_stats[home_goalie_stats.situation!="all"].index)
				home_goalie_stats=home_goalie_stats.drop(home_goalie_stats[home_goalie_stats.season<current_season-2].index)
				days_since_last_game=str(todays_date-int(home_goalie_stats.iloc[[-1]]["gameDate"]))
#
				home_goalie_stats['highDangerSavePercentage']=home_goalie_stats['highDangerGoals']/home_goalie_stats['highDangerShots']
#				print(home_goalie_stats['highDangerSavePercentage'])
				home_goalie_stats['mediumDangerSavePercentage']=home_goalie_stats['mediumDangerGoals']/home_goalie_stats['mediumDangerShots']
				home_goalie_stats['lowDangerSavePercentage']=home_goalie_stats['lowDangerGoals']/home_goalie_stats['lowDangerShots']
				home_goalie_stats['highDangerSavePercentage'].fillna(1, inplace=True)
#				print(home_goalie_stats['highDangerSavePercentage'])
				home_goalie_stats['mediumDangerSavePercentage'].fillna(1, inplace=True)
				home_goalie_stats['lowDangerSavePercentage'].fillna(1, inplace=True)
				mlr_high_danger_SVP=LinearRegression()
				mlr_medium_danger_SVP=LinearRegression()
				mlr_low_danger_SVP=LinearRegression()
				mlr_high_danger_SVP.fit(home_goalie_stats[[away_team, "HOME", day_of_week, "days_since_last_game_"+days_since_last_game]], home_goalie_stats['highDangerSavePercentage'])
				mlr_medium_danger_SVP.fit(home_goalie_stats[[away_team, "HOME", day_of_week, "days_since_last_game_"+days_since_last_game]], home_goalie_stats['mediumDangerSavePercentage'])
				mlr_low_danger_SVP.fit(home_goalie_stats[[away_team, "HOME", day_of_week, "days_since_last_game_"+days_since_last_game]], home_goalie_stats['lowDangerSavePercentage'])


				if home_goalie_stats[away_team].sum() == 0:
					Opp_coef=0
				else:
					Opp_coef=1
				if home_goalie_stats["HOME"].sum() == 0:
					H_A_coef=0
				else:
					H_A_coef=1
				if home_goalie_stats[day_of_week].sum() == 0:
					DOW_coef=0
				else:
					DOW_coef=1	


				xHD_SVP = mlr_high_danger_SVP.intercept_ + mlr_high_danger_SVP.coef_[0] + mlr_high_danger_SVP.coef_[1] + mlr_high_danger_SVP.coef_[2] + mlr_high_danger_SVP.coef_[3]
				xMD_SVP = mlr_medium_danger_SVP.intercept_ + mlr_medium_danger_SVP.coef_[0] + mlr_medium_danger_SVP.coef_[1] + mlr_medium_danger_SVP.coef_[2] + mlr_medium_danger_SVP.coef_[3] 
				xLD_SVP = mlr_low_danger_SVP.intercept_ + mlr_low_danger_SVP.coef_[0] + mlr_low_danger_SVP.coef_[1] + mlr_low_danger_SVP.coef_[2] + mlr_low_danger_SVP.coef_[3] 

			else:
				print("No stats for goalie %s, goalie calculations cannot be made" % home_goalie)

			if os.path.isfile(('g2g_stats_moneypuck/%s.csv') % away_goalie):
				away_goalie_stats=pd.read_csv("g2g_stats_moneypuck/%s.csv" % (away_goalie))
				away_goalie_stats=clean_df(away_goalie_stats, "AWAY", day_of_week, todays_date, home_team, current_season)
				away_goalie_stats=away_goalie_stats.drop(away_goalie_stats[away_goalie_stats.situation!="all"].index)
				away_goalie_stats=away_goalie_stats.drop(away_goalie_stats[away_goalie_stats.season<current_season-2].index)
			else:
				print("No stats for goalie %s, goalie calculations cannot be made" % away_goalie)




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

	stats=clean_df(stats, Home_or_Away, Day_of_week, todays_date, Opp, current_season)
	
	if type(stats)==bool:
		return False
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

	xeven_list = perform_shot_metric_calculations(stats_5on5, Home_or_Away, Day_of_week, todays_date, Opp, current_season)
	xevenGF=xeven_list[0]
	xevenGA=xeven_list[1]
	if print_individual_stats==True:
		print("Expected Even Strength Goals For = %s" % (xevenGF))
		print("Expected Even Strength Goals Against = %s" % (xevenGA))
	xPP_list = perform_shot_metric_calculations(stats_5on4, Home_or_Away, Day_of_week, todays_date, Opp, current_season)
	xPPGF=xPP_list[0]
	xSHGA=xPP_list[1]
	if print_individual_stats==True:
		print("Expected PP Goals For = %s" % (xPPGF))
		print("Expected SH Goals Against = %s" % (xSHGA))
	xSH_list = perform_shot_metric_calculations(stats_4on5, Home_or_Away, Day_of_week, todays_date, Opp, current_season)
	xSHGF=xSH_list[0]
	xPPGA=xSH_list[1]
	if print_individual_stats==True:
		print("Expected SH Goals For = %s" % (xSHGF))
		print("Expected PP Goals Against = %s" % (xPPGA))
	
	xHDA=xeven_list[2]/5+xPP_list[2]/5+xSH_list[2]/4
	xMDA=xeven_list[3]/5+xPP_list[3]/5+xSH_list[3]/4
	xLDA=xeven_list[4]/5+xPP_list[4]/5+xSH_list[4]/4
	return_list= [xevenGF, xevenGA, xPPGF, xSHGA, xSHGF, xPPGA, xHDA, xMDA, xLDA]
	return return_list






def perform_shot_metric_calculations(df, Home_or_Away, Day_of_week, todays_date, Opp, current_season):


	### This calculates the average time on ice
	AVG_TOI=df['icetime'].sum()/df.shape[0]
	
	### Creates the linear regression objects
	mlr_high_danger_for=LinearRegression()
	mlr_medium_danger_for=LinearRegression()
	mlr_low_danger_for=LinearRegression()
	mlr_high_danger_against=LinearRegression()
	mlr_medium_danger_against=LinearRegression()
	mlr_low_danger_against=LinearRegression()
	
	days_since_last_game=str(todays_date-int(df.iloc[[-1]]["gameDate"]))

	### Creates the prediction system for each type of shot
	mlr_high_danger_for.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game]], df['OnIce_F_highDangerShots'])
	mlr_medium_danger_for.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game]], df['OnIce_F_mediumDangerShots'])
	mlr_low_danger_for.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game]], df['OnIce_F_lowDangerShots'])
	mlr_high_danger_against.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game]], df['OnIce_A_highDangerShots'])
	mlr_medium_danger_against.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game]], df['OnIce_A_mediumDangerShots'])
	mlr_low_danger_against.fit(df[[Opp, Home_or_Away, 'icetime', Day_of_week, "days_since_last_game_"+days_since_last_game]], df['OnIce_A_lowDangerShots'])

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
	if df[Opp].sum() == 0:
		Opp_coef=0
	else:
		Opp_coef=1
	if df[Home_or_Away].sum() == 0:
		H_A_coef=0
	else:
		H_A_coef=1
	if df[Day_of_week].sum() == 0:
		DOW_coef=0
	else:
		DOW_coef=1	

	xHDF = mlr_high_danger_for.intercept_ + Opp_coef*mlr_high_danger_for.coef_[0] + H_A_coef*mlr_high_danger_for.coef_[1] + AVG_TOI*mlr_high_danger_for.coef_[2] + DOW_coef*mlr_high_danger_for.coef_[3] + mlr_high_danger_for.coef_[4]
#	print(mlr_high_danger_for.coef_[0])
#	print(mlr_high_danger_for.coef_[1])
#	print(mlr_high_danger_for.coef_[2])
#	print(mlr_high_danger_for.coef_[3])
#	print(mlr_high_danger_for.coef_[4])
	xMDF = mlr_medium_danger_for.intercept_ + Opp_coef*mlr_medium_danger_for.coef_[0] + H_A_coef*mlr_medium_danger_for.coef_[1] + AVG_TOI*mlr_medium_danger_for.coef_[2] + DOW_coef*mlr_medium_danger_for.coef_[3] + mlr_medium_danger_for.coef_[4]
	xLDF = mlr_low_danger_for.intercept_ + Opp_coef*mlr_low_danger_for.coef_[0] + H_A_coef*mlr_low_danger_for.coef_[1] + AVG_TOI*mlr_low_danger_for.coef_[2] + DOW_coef*mlr_low_danger_for.coef_[3] + mlr_low_danger_for.coef_[4]
	xHDA = mlr_high_danger_against.intercept_ + Opp_coef*mlr_high_danger_against.coef_[0] + H_A_coef*mlr_high_danger_against.coef_[1] + AVG_TOI*mlr_high_danger_against.coef_[2] + DOW_coef*mlr_high_danger_against.coef_[3] + mlr_high_danger_against.coef_[4]
	xMDA = mlr_medium_danger_against.intercept_ + Opp_coef*mlr_medium_danger_against.coef_[0] + H_A_coef*mlr_medium_danger_against.coef_[1] + AVG_TOI*mlr_medium_danger_against.coef_[2] + DOW_coef*mlr_medium_danger_against.coef_[3] + mlr_medium_danger_against.coef_[4]
	xLDA = mlr_low_danger_against.intercept_ + Opp_coef*mlr_low_danger_against.coef_[0] + H_A_coef*mlr_low_danger_against.coef_[1] + AVG_TOI*mlr_low_danger_against.coef_[2] + DOW_coef*mlr_low_danger_against.coef_[3] + mlr_low_danger_against.coef_[4]
	
	### This part calculates how many goals for and against the player will be on for
	#print("xGF= %s*%s + %s*%s + %s*%s" % (xHDF, high_danger_for_efficiency, xMDF, medium_danger_for_efficiency, xLDF, low_danger_for_efficiency))
	xGF= xHDF*high_danger_for_efficiency + xMDF*medium_danger_for_efficiency + xLDF*low_danger_for_efficiency
	xGA= xHDA*high_danger_against_efficiency + xMDA*medium_danger_against_efficiency + xLDA*low_danger_against_efficiency
	
	### Uncomment to print the specific expected goals for and against for this player
	#print(player)

	return_list = [xGF, xGA, xHDA, xMDA, xLDA]
	xGF, xGA

	return return_list


def clean_df(df, Home_or_Away, Day_of_week, todays_date, Opp, current_season):
	new_df=df
	new_df.sort_values(by = 'gameDate', inplace= True)
	new_df['day_of_week']=new_df['gameDate'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d').strftime('%A'))
	

	new_df=pd.get_dummies(new_df, columns=['home_or_away'], prefix='', prefix_sep='')
	new_df=pd.get_dummies(new_df, columns=['opposingTeam'], prefix='', prefix_sep='')
	new_df=pd.get_dummies(new_df, columns=['day_of_week'], prefix='', prefix_sep='')

#away_goalie_stats[away_goalie_stats.situation!="all"].index
	if allow_past_analysis:
		new_df.drop(new_df[new_df.gameDate>=todays_date].index, inplace=True)
	days_between_games_list=count_days_between_games_moneypuck(new_df['gameDate'])
	new_df['days_since_last_game']=days_between_games_list
	new_df=pd.get_dummies(new_df, columns=['days_since_last_game'], prefix=None)

	### If a player has never been in a certain situation (eg. never played game on wednesday) then variable is set to 0 for all rows
	if Opp not in new_df.columns:
		new_df[Opp]=np.zeros(new_df.shape[0], dtype=int)
	if Home_or_Away not in new_df.columns:
		new_df[Home_or_Away]=np.zeros(new_df.shape[0], dtype=int)
	if Day_of_week not in new_df.columns:
		new_df[Day_of_week]=np.zeros(new_df.shape[0], dtype=int)

	if len(new_df.index) < 20*5:
		return False
#	print(new_df.iloc[[-1]]['gameDate'])
	days_since_last_game=str(todays_date-int(new_df.iloc[[-1]]["gameDate"]))
	if (int(days_since_last_game)<1):
		print("Incorrect input for game date: Aborting")
		quit()
	if "days_since_last_game_"+days_since_last_game not in new_df.columns:
		new_df["days_since_last_game_"+days_since_last_game]=np.zeros(new_df.shape[0], dtype=int)

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







def goalie_scoring_analysis_moneypuck():
	None


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


