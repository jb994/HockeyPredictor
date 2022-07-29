#!/usr/bin/env

# V 1.0

### NOTE: Next Step
# I want to make a stat or each team that will be a multiplier
# The stat is CA/GA to see how impactful corsi against a certain team is.
# Hopefully I can use this to modify how likely a team is to score against them based
# On a high CF

import os
import numpy as np
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
from datetime import date as getDate

debug=False
printIndividualStats=True # Prints the individual predicted stats for each player
calculatePenalties=False # Unavailable
doGoalieAnalysis=False # Will perform an additional goalie stat analysis at the end
allowPastAnalysis=True # Let's the user put in game's from a past date, assuming the correct roster is used

def gameCalculation(homeTeam, awayTeam, date, season, doRefAnalysis=False):
	### A multiple variable linear regression software used to predict the outcomes of hockey games
	

	#################################################################
	### Please insert the variables below to perform the analysis ###
	#################################################################
	# [['ANA','ARI','BOS','BUF','CAR','CBJ','CGY','CHI','COL','DAL','DET','EDM','FLA','L.A','MIN','MTL','N.J','NSH','NYI','NYR','OTT','PHI','PIT','S.J','STL','T.B','TOR','VAN','VGK','WPG','WSH']]
	gameDay=str(date)
	dayOfWeek=getDate(int(gameDay[0:4]), int(gameDay[4:6]), int(gameDay[6:8])).strftime("%A")
	#dayOfWeek='Sunday' # [["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]
	if doRefAnalysis:
		ref1='name' #First ref's name
		ref2='name' #Second ref's name
		refFile=open("ref_%s_stats.csv" % (season))
	else:
		refFile=None


	gameInfo={
		'homeTeam':homeTeam,
		'awayTeam':awayTeam,
		'dayOfWeek':dayOfWeek,
		'date':date,
		'season':season
	}

	team_analysis_w_moneypuck(gameInfo)
	
	if refFile != None:
		refFile.close()





def team_analysis_w_moneypuck(gameInfo):
	### This function predicts how many goals each team is supposed to score and let in by \
	### using regression analysis to determine how many high, medium, and low scoring chances\
	### each player will get and how many they will capitalize on.
	homeTeamRosterFile=open("team_rosters/%s" % (gameInfo['homeTeam']))
	awayTeamRosterFile=open("team_rosters/%s" % (gameInfo['awayTeam']))

	### Initializes all the variables used to record predicted stats
	homeTeamxPEN=0
	awayTeamxPEN=0

	homeTeamxGF=0
	homeTeamxGA=0
	homeTeamxPPGF=0
	homeTeamxSHGA=0
	homeTeamxSHGF=0
	homeTeamxPPGA=0
	homeTeamxHDA=0
	homeTeamxMDA=0
	homeTeamxLDA=0
	awayTeamxGF=0
	awayTeamxGA=0
	awayTeamxPPGF=0
	awayTeamxSHGA=0
	awayTeamxSHGF=0
	awayTeamxPPGA=0
	awayTeamxHDA=0
	awayTeamxMDA=0
	awayTeamxLDA=0

	
	homeTeamRoster=homeTeamRosterFile.readlines()
	awayTeamRoster=awayTeamRosterFile.readlines()

########################################################################
	if calculatePenalties==True:
	### Not yet up
		### Predicts home team minor penalties
		homeTeamxPen, awayTeamxPen = doPenaltyAnalysis(homeTeamRoster, awayTeamRoster, gameInfo)

		print("Number of penalties by home team = " + str(homeTeamXPEN))
		print("Number of penalties by away team = " + str(awayTeamXPEN))
		print("")
##########################################################################


	### Analysis of Home Team to estimate how many goals for and goals against
	for index in range(18):
		player=homeTeamRoster[index].replace("\n",'')
		homeTeamGoalMetricsList=playerScoringAnalysisMoneypuck(player, "HOME", gameInfo)
		# Returns list in form [xevenGF, xevenGA, xPPGF, xSHGA, xSHGF, xPPGA]
		homeTeamxGF=homeTeamxGF+homeTeamGoalMetricsList[0]
		homeTeamxGA=homeTeamxGA+homeTeamGoalMetricsList[1]
		homeTeamxPPGF=homeTeamxPPGF+homeTeamGoalMetricsList[2]
		homeTeamxSHGA=homeTeamxSHGA+homeTeamGoalMetricsList[3]
		homeTeamxSHGF=homeTeamxSHGF+homeTeamGoalMetricsList[4]
		homeTeamxPPGA=homeTeamxPPGA+homeTeamGoalMetricsList[5]
		homeTeamxHDA=homeTeamxHDA+homeTeamGoalMetricsList[6]
		homeTeamxMDA=homeTeamxMDA+homeTeamGoalMetricsList[7]
		homeTeamxLDA=homeTeamxLDA+homeTeamGoalMetricsList[8]
	print("")

	### Analysis of Away Team to estimate how many goals for and against
	for index in range(18):
		player=awayTeamRoster[index].replace('\n','')
		awayTeamGoalMetricsList=playerScoringAnalysisMoneypuck(player, "AWAY", gameInfo)
		# Returns list in form [xevenGF, xevenGA, xPPGF, xSHGA, xSHGF, xPPGA]
		awayTeamxGF=awayTeamxGF+awayTeamGoalMetricsList[0]
		awayTeamxGA=awayTeamxGA+awayTeamGoalMetricsList[1]
		awayTeamxPPGF=awayTeamxPPGF+awayTeamGoalMetricsList[2]
		awayTeamxSHGA=awayTeamxSHGA+awayTeamGoalMetricsList[3]
		awayTeamxSHGF=awayTeamxSHGF+awayTeamGoalMetricsList[4]
		awayTeamxPPGA=awayTeamxPPGA+awayTeamGoalMetricsList[5]
		awayTeamxHDA=awayTeamxHDA+awayTeamGoalMetricsList[6]
		awayTeamxMDA=awayTeamxMDA+awayTeamGoalMetricsList[7]
		awayTeamxLDA=awayTeamxLDA+awayTeamGoalMetricsList[8]
	print("")

	print("Expected Even Strength Goals For Home Team: %s" % (homeTeamxGF/5))
	print("Expected Even Strength Goals Against Home Team: %s" % (homeTeamxGA/5))
	print("Expected Power Play Goals For Home Team: %s" % (homeTeamxPPGF/5))
	print("Expected Short Handed Goals Against Home Team: %s" % (homeTeamxSHGA/5))
	print("Expected Short Handed Goals For Home Team: %s" % (homeTeamxSHGF/4))
	print("Expected Power Play Goals Against Home Team: %s" % (homeTeamxPPGA/4))
	print("Total Expected Goals For Home Team = %s" % (homeTeamxGF/5 + homeTeamxPPGF/5 + homeTeamxSHGF/4))
	print("Total Expected Goals Against Home Team = %s" % (homeTeamxGA/5 + homeTeamxSHGA/5 + homeTeamxPPGA/4))
	print("")

	print("Expected Even Strength Goals For Away Team: %s" % (awayTeamxGF/5))
	print("Expected Even Strength Goals Against Away Team: %s" % (awayTeamxGA/5))
	print("Expected Power Play Goals For Away Team: %s" % (awayTeamxPPGF/5))
	print("Expected Short Handed Goals Against Away Team: %s" % (awayTeamxSHGA/5))
	print("Expected Short Handed Goals For Away Team: %s" % (awayTeamxSHGF/4))
	print("Expected Power Play Goals Against Away Team: %s" % (awayTeamxPPGA/4))
	print("Total Expected Goals For Away Team = %s" % (awayTeamxGF/5 + awayTeamxPPGF/5 + awayTeamxSHGF/4))
	print("Total Expected Goals Against Away Team = %s" % (awayTeamxGA/5 + awayTeamxSHGA/5 + awayTeamxPPGA/4))
	print("")


	if doGoalieAnalysis==True:
		if len(homeTeamRoster)!=19 or len(awayTeamRoster)!=19:
			print("Goalie analysis cannot be conducted because name of goalie is missing")
		else:
			homeGoalie=homeTeamRoster[18].replace("\n",'')
			awayGoalie=awayTeamRoster[18].replace("\n",'')
			if os.path.isfile(('moneypuckPlayerStats/%s.csv') % homeGoalie):
				goalieAnalysis()

				homeGoalieStats=pd.read_csv("moneypuckPlayerStats/%s.csv" % (homeGoalie))
				homeGoalieStats=clean_df(homeGoalieStats, "HOME", gameInfo)
				homeGoalieStats=homeGoalieStats.drop(homeGoalieStats[homeGoalieStats.situation!="all"].index)
				homeGoalieStats=homeGoalieStats.drop(homeGoalieStats[homeGoalieStats.season<gameInfo['season']-2].index)
				daysSinceLastGame=str(gameInfo['date']-int(homeGoalieStats.iloc[[-1]]["gameDate"]))

				homeGoalieStats['highDangerSavePercentage']=homeGoalieStats['highDangerGoals']/homeGoalieStats['highDangerShots']
				homeGoalieStats['mediumDangerSavePercentage']=homeGoalieStats['mediumDangerGoals']/homeGoalieStats['mediumDangerShots']
				homeGoalieStats['lowDangerSavePercentage']=homeGoalieStats['lowDangerGoals']/homeGoalieStats['lowDangerShots']
				homeGoalieStats['highDangerSavePercentage'].fillna(1, inplace=True)
				homeGoalieStats['mediumDangerSavePercentage'].fillna(1, inplace=True)
				homeGoalieStats['lowDangerSavePercentage'].fillna(1, inplace=True)
				mlrHighDangerSVP=LinearRegression()
				mlrMediumDangerSVP=LinearRegression()
				mlrLowDangerSVP=LinearRegression()
				mlrHighDangerSVP.fit(homeGoalieStats[[gameInfo['awayTeam'], "HOME", gameInfo['dayOfWeek'], "daysSinceLastGame_"+daysSinceLastGame]], homeGoalieStats['highDangerSavePercentage'])
				mlrMediumDangerSVP.fit(homeGoalieStats[[gameInfo['awayTeam'], "HOME", gameInfo['dayOfWeek'], "daysSinceLastGame_"+daysSinceLastGame]], homeGoalieStats['mediumDangerSavePercentage'])
				mlrLowDangerSVP.fit(homeGoalieStats[[gameInfo['awayTeam'], "HOME", gameInfo['dayOfWeek'], "daysSinceLastGame_"+daysSinceLastGame]], homeGoalieStats['lowDangerSavePercentage'])


				if homeGoalieStats[gameInfo['awayTeam']].sum() == 0:
					oppCoef=0
				else:
					oppCoef=1
				if homeGoalieStats["HOME"].sum() == 0:
					H_A_coef=0
				else:
					H_A_coef=1
				if homeGoalieStats[gameInfo['dayOfWeek']].sum() == 0:
					DOW_coef=0
				else:
					DOW_coef=1	


				xHD_SVP = mlrHighDangerSVP.intercept_ + mlrHighDangerSVP.coef_[0] + mlrHighDangerSVP.coef_[1] + mlrHighDangerSVP.coef_[2] + mlrHighDangerSVP.coef_[3]
				xMD_SVP = mlrMediumDangerSVP.intercept_ + mlrMediumDangerSVP.coef_[0] + mlrMediumDangerSVP.coef_[1] + mlrMediumDangerSVP.coef_[2] + mlrMediumDangerSVP.coef_[3] 
				xLD_SVP = mlrLowDangerSVP.intercept_ + mlrLowDangerSVP.coef_[0] + mlrLowDangerSVP.coef_[1] + mlrLowDangerSVP.coef_[2] + mlrLowDangerSVP.coef_[3] 

			else:
				print("No stats for goalie %s, goalie calculations cannot be made" % homeGoalie)

			if os.path.isfile(('moneypuckPlayerStats/%s.csv') % awayGoalie):
				awayGoalieStats=pd.read_csv("moneypuckPlayerStats/%s.csv" % (awayGoalie))
				awayGoalieStats=clean_df(awayGoalieStats, "AWAY", gameInfo)
				awayGoalieStats=awayGoalieStats.drop(awayGoalieStats[awayGoalieStats.situation!="all"].index)
				awayGoalieStats=awayGoalieStats.drop(awayGoalieStats[awayGoalieStats.season<gameInfo['season']-2].index)
			else:
				print("No stats for goalie %s, goalie calculations cannot be made" % awayGoalie)




def playerScoringAnalysisMoneypuck(player, homeOrAway, gameInfo):
	### This analysis takes all the stats from a player and calculate how many expected high, medium, and low quality shots\
	### they will be on the ice for in a game. Variables like whether it is a home or away game, the day of the week, days\
	### since the last game, the player's history against this certain opponent.
	### The shooting percentage for each type of shot is then calculated and an overall stat of how many goals the player\
	### will be on the ice for is calculated.

	### Checks that the player's stat file exists, if not then the program quits
	if homeOrAway=='HOME':
		opp=gameInfo['awayTeam']
	else:
		opp=gameInfo['homeTeam']

	try:
		stats=pd.read_csv("moneypuckPlayerStats/%s.csv" % (player))
	except:
		print("No stats for player %s, prediction cannot be made: Aborting" % player)
		quit()

	print(player)
	stats=clean_df(stats, homeOrAway, gameInfo)
	
	
	### Removes stats that are for situations that are not 5on5 or that are over 2 years ago
	stats5on5=stats.drop(stats[stats.situation!="5on5"].index)
	stats5on5=stats5on5.drop(stats5on5[stats5on5.season<gameInfo['season']-2].index)
	stats5on4=stats.drop(stats[stats.situation!="5on4"].index)
	stats5on4=stats5on4.drop(stats5on4[stats5on4.season<gameInfo['season']-2].index)
	stats4on5=stats.drop(stats[stats.situation!="4on5"].index)
	stats4on5=stats4on5.drop(stats4on5[stats4on5.season<gameInfo['season']-2].index)

	#stats_5on5=clean_df(stats_5on5)
	#stats_5on4=clean_df(stats_5on4)
	#stats_4on5=clean_df(stats_4on5)

	#scipy.stats.pearsonr(stats_5on5[''])
	### Adds a variable that contains the day of the week each game was on
	#stats_5on5['day_of_week']=stats_5on5['gameDate'].apply(lambda x: datetime.strptime(str(x),'%Y%m%d').strftime('%A'))

	xEvenList = shotMetricCalculations(stats5on5, opp, homeOrAway, gameInfo)
	xEvenGF=xEvenList[0]
	xEvenGA=xEvenList[1]
	if printIndividualStats==True:
		print("Expected Even Strength Goals For = %s" % (xEvenGF))
		print("Expected Even Strength Goals Against = %s" % (xEvenGA))
	xPPList = shotMetricCalculations(stats5on4, opp, homeOrAway, gameInfo)
	xPPGF=xPPList[0]
	xSHGA=xPPList[1]
	if printIndividualStats==True:
		print("Expected PP Goals For = %s" % (xPPGF))
		print("Expected SH Goals Against = %s" % (xSHGA))
	xSHList = shotMetricCalculations(stats4on5, opp, homeOrAway, gameInfo)
	xSHGF=xSHList[0]
	xPPGA=xSHList[1]
	if printIndividualStats==True:
		print("Expected SH Goals For = %s" % (xSHGF))
		print("Expected PP Goals Against = %s" % (xPPGA))
	
	xHDA=xEvenList[2]/5+xPPList[2]/5+xSHList[2]/4
	xMDA=xEvenList[3]/5+xPPList[3]/5+xSHList[3]/4
	xLDA=xEvenList[4]/5+xPPList[4]/5+xSHList[4]/4
	returnList= [xEvenGF, xEvenGA, xPPGF, xSHGA, xSHGF, xPPGA, xHDA, xMDA, xLDA]
	return returnList






def shotMetricCalculations(df, opp, homeOrAway, gameInfo):

	if homeOrAway=='HOME':
		opp=gameInfo['awayTeam']
	else:
		opp=gameInfo['homeTeam']

	### This calculates the average time on ice
	avgTOI=df['icetime'].sum()/df.shape[0]
	
	### Creates the linear regression objects
	mlrHighDangerFor=LinearRegression()
	mlrMediumDangerFor=LinearRegression()
	mlrLowDangerFor=LinearRegression()
	mlrHighDangerAgainst=LinearRegression()
	mlrMediumDangerAgainst=LinearRegression()
	mlrLowDangerAgainst=LinearRegression()

	### Get the value for how many days its been since the prior game
	daysSinceLastGame=str(gameInfo['date']-int(df.iloc[[-1]]["gameDate"]))
	if int(daysSinceLastGame)>7:
		daysSinceLastGame='7'

	### Creates the prediction system for each type of shot
	mlrHighDangerFor.fit(df[[opp, homeOrAway, 'icetime', gameInfo['dayOfWeek'], "daysSinceLastGame_"+daysSinceLastGame]], df['OnIce_F_highDangerShots'])
	mlrMediumDangerFor.fit(df[[opp, homeOrAway, 'icetime', gameInfo['dayOfWeek'], "daysSinceLastGame_"+daysSinceLastGame]], df['OnIce_F_mediumDangerShots'])
	mlrLowDangerFor.fit(df[[opp, homeOrAway, 'icetime', gameInfo['dayOfWeek'], "daysSinceLastGame_"+daysSinceLastGame]], df['OnIce_F_lowDangerShots'])
	mlrHighDangerAgainst.fit(df[[opp, homeOrAway, 'icetime', gameInfo['dayOfWeek'], "daysSinceLastGame_"+daysSinceLastGame]], df['OnIce_A_highDangerShots'])
	mlrMediumDangerAgainst.fit(df[[opp, homeOrAway, 'icetime', gameInfo['dayOfWeek'], "daysSinceLastGame_"+daysSinceLastGame]], df['OnIce_A_mediumDangerShots'])
	mlrLowDangerAgainst.fit(df[[opp, homeOrAway, 'icetime', gameInfo['dayOfWeek'], "daysSinceLastGame_"+daysSinceLastGame]], df['OnIce_A_lowDangerShots'])

	### Calculates how often a high/medium/low quality shot for goes in while this player is on the ice
	highDangerForEfficiency = float(df['OnIce_F_highDangerGoals'].sum()) / float(df['OnIce_F_highDangerShots'].sum()) if df['OnIce_F_highDangerShots'].sum() else 0
	mediumDangerForEfficiency = float(df['OnIce_F_mediumDangerGoals'].sum()) / float(df['OnIce_F_mediumDangerShots'].sum()) if df['OnIce_F_mediumDangerShots'].sum() else 0
	lowDangerForEfficiency = float(df['OnIce_F_lowDangerGoals'].sum()) / float(df['OnIce_F_lowDangerShots'].sum()) if df['OnIce_F_lowDangerShots'].sum() else 0
	highDangerAgainstEfficiency = float(df['OnIce_A_highDangerGoals'].sum()) / float(df['OnIce_A_highDangerShots'].sum()) if df['OnIce_A_highDangerShots'].sum() else 0
	mediumDangerAgainstEfficiency = float(df['OnIce_A_mediumDangerGoals'].sum()) / float(df['OnIce_A_mediumDangerShots'].sum()) if df['OnIce_A_mediumDangerShots'].sum() else 0
	lowDangerAgainstEfficiency = float(df['OnIce_A_lowDangerGoals'].sum()) / float(df['OnIce_A_lowDangerShots'].sum()) if df['OnIce_A_lowDangerShots'].sum() else 0

	if debug:
		print(str(mlrHighDangerFor.intercept_)+ ' ' + str(mlrHighDangerFor.coef_[0]) + ' ' + str(mlrHighDangerFor.coef_[1]) + ' ' + str(avgTOI*mlrHighDangerFor.coef_[2]) + ' ' + str(mlrHighDangerFor.coef_[3]) + ' ' + str(mlrHighDangerFor.coef_[4]))
		print(str(mlrMediumDangerFor.intercept_) + ' ' + str(mlrMediumDangerFor.coef_[0]) + ' ' + str(mlrMediumDangerFor.coef_[1]) + ' ' + str(avgTOI*mlrMediumDangerFor.coef_[2]) + ' ' + str(mlrMediumDangerFor.coef_[3]) + ' ' + str(mlrMediumDangerFor.coef_[4]))
		print(str(mlrLowDangerFor.intercept_) + ' ' + str(mlrLowDangerFor.coef_[0]) + ' ' + str(mlrLowDangerFor.coef_[1]) + ' ' + str(avgTOI*mlrLowDangerFor.coef_[2]) + ' ' + str(mlrLowDangerFor.coef_[3]) + ' ' + str(mlrLowDangerFor.coef_[4]))
		print(str(mlrHighDangerAgainst.intercept_) + ' ' + str(mlrHighDangerAgainst.coef_[0]) + ' ' + str(mlrHighDangerAgainst.coef_[1]) + ' ' + str(avgTOI*mlrHighDangerAgainst.coef_[2]) + ' ' + str(mlrHighDangerAgainst.coef_[3]) + ' ' + str(mlrHighDangerAgainst.coef_[4]))
		print(str(mlrMediumDangerAgainst.intercept_) + ' ' + str(mlrMediumDangerAgainst.coef_[0]) + ' ' + str(mlrMediumDangerAgainst.coef_[1]) + ' ' + str(avgTOI*mlrMediumDangerAgainst.coef_[2]) + ' ' + str(mlrMediumDangerAgainst.coef_[3]) + ' ' + str(mlrMediumDangerAgainst.coef_[4]))
		print(str(mlrLowDangerAgainst.intercept_ )+ ' ' + str(mlrLowDangerAgainst.coef_[0]) + ' ' + str(mlrLowDangerAgainst.coef_[1]) + ' ' + str(avgTOI*mlrLowDangerAgainst.coef_[2]) + ' ' + str(mlrLowDangerAgainst.coef_[3]) + ' ' + str(mlrLowDangerAgainst.coef_[4]))

	### Does the actual calculation for expected high/medium/low shots for/against the player's team while he is on the ice
	if df[opp].sum() == 0:
		oppCoef=0
	else:
		oppCoef=1
	if df[homeOrAway].sum() == 0:
		H_A_coef=0
	else:
		H_A_coef=1
	if df[gameInfo['dayOfWeek']].sum() == 0:
		DOW_coef=0
	else:
		DOW_coef=1	

	xHDF = mlrHighDangerFor.intercept_ + oppCoef*mlrHighDangerFor.coef_[0] + H_A_coef*mlrHighDangerFor.coef_[1] + avgTOI*mlrHighDangerFor.coef_[2] + DOW_coef*mlrHighDangerFor.coef_[3] + mlrHighDangerFor.coef_[4]
	xMDF = mlrMediumDangerFor.intercept_ + oppCoef*mlrMediumDangerFor.coef_[0] + H_A_coef*mlrMediumDangerFor.coef_[1] + avgTOI*mlrMediumDangerFor.coef_[2] + DOW_coef*mlrMediumDangerFor.coef_[3] + mlrMediumDangerFor.coef_[4]
	xLDF = mlrLowDangerFor.intercept_ + oppCoef*mlrLowDangerFor.coef_[0] + H_A_coef*mlrLowDangerFor.coef_[1] + avgTOI*mlrLowDangerFor.coef_[2] + DOW_coef*mlrLowDangerFor.coef_[3] + mlrLowDangerFor.coef_[4]
	xHDA = mlrHighDangerAgainst.intercept_ + oppCoef*mlrHighDangerAgainst.coef_[0] + H_A_coef*mlrHighDangerAgainst.coef_[1] + avgTOI*mlrHighDangerAgainst.coef_[2] + DOW_coef*mlrHighDangerAgainst.coef_[3] + mlrHighDangerAgainst.coef_[4]
	xMDA = mlrMediumDangerAgainst.intercept_ + oppCoef*mlrMediumDangerAgainst.coef_[0] + H_A_coef*mlrMediumDangerAgainst.coef_[1] + avgTOI*mlrMediumDangerAgainst.coef_[2] + DOW_coef*mlrMediumDangerAgainst.coef_[3] + mlrMediumDangerAgainst.coef_[4]
	xLDA = mlrLowDangerAgainst.intercept_ + oppCoef*mlrLowDangerAgainst.coef_[0] + H_A_coef*mlrLowDangerAgainst.coef_[1] + avgTOI*mlrLowDangerAgainst.coef_[2] + DOW_coef*mlrLowDangerAgainst.coef_[3] + mlrLowDangerAgainst.coef_[4]
	
	### This part calculates how many goals for and against the player will be on for
	xGF= xHDF*highDangerForEfficiency + xMDF*mediumDangerForEfficiency + xLDF*lowDangerForEfficiency
	xGA= xHDA*highDangerAgainstEfficiency + xMDA*mediumDangerAgainstEfficiency + xLDA*lowDangerAgainstEfficiency

	returnList = [xGF, xGA, xHDA, xMDA, xLDA]
	xGF, xGA

	return returnList



#def clean_df(df, Home_or_Away, Day_of_week, todays_date, Opp, current_season):
def clean_df(df, homeOrAway, gameInfo):

	if homeOrAway=='HOME':
		opp=gameInfo['awayTeam']
	else:
		opp=gameInfo['homeTeam']

	newDF=df
	newDF.sort_values(by = 'gameDate', inplace= True)
	newDF['dayOfWeek']=newDF['gameDate'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d').strftime('%A'))
	

	#newDF = pd.get_dummies(newDF, columns=['homeOrAway', 'opposingTeam', 'dayOfWeek'], prefix='', prefix_sep='')
	newDF=pd.get_dummies(newDF, columns=['home_or_away', 'opposingTeam', 'dayOfWeek'], prefix='', prefix_sep='')
	#newDF=pd.get_dummies(newDF, columns=['opposingTeam'], prefix='', prefix_sep='')
	#newDF=pd.get_dummies(newDF, columns=['dayOfWeek'], prefix='', prefix_sep='')

	if allowPastAnalysis:
		newDF.drop(newDF[newDF.gameDate>=gameInfo['date']].index, inplace=True)
	daysBetweenGamesList=countDaysBetweenGamesMoneypuck(newDF['gameDate'])
	newDF['daysSinceLastGame']=daysBetweenGamesList
	newDF=pd.get_dummies(newDF, columns=['daysSinceLastGame'], prefix=None)

	### If a player has never been in a certain situation (eg. never played game on wednesday) then variable is set to 0 for all rows
	if opp not in newDF.columns:
		newDF[opp]=np.zeros(newDF.shape[0], dtype=int)
	if homeOrAway not in newDF.columns:
		newDF[homeOrAway]=np.zeros(newDF.shape[0], dtype=int)
	if gameInfo['dayOfWeek'] not in newDF.columns:
		newDF[gameInfo['dayOfWeek']]=np.zeros(newDF.shape[0], dtype=int)
	daysSinceLastGame=str(gameInfo['date']-int(newDF.iloc[[-1]]["gameDate"]))
	if (int(daysSinceLastGame)<1):
		print("Incorrect input for game date: Aborting")
		quit()
	if "daysSinceLastGame_"+daysSinceLastGame not in newDF.columns:
		newDF["daysSinceLastGame_"+daysSinceLastGame]=np.zeros(newDF.shape[0], dtype=int)

	return newDF



def doPenaltyAnalysis(homeTeamRoster, awayTeamRoster, gameInfo):
	for index in range(18):
		player=homeTeamRoster[index].replace("\n",'')
		playerPenalties=LinearRegression()
		try:
			stats=pd.read_csv("moneypuckPlayerStats/%s.csv" % (player))
		except:
			print("No stats for player %s, prediction cannot be made: Aborting" % player)
			quit()

		xPEN=calcxPenalties(stats, "HOME", gameInfo)
		homeTeamXPEN=homeTeamXPEN+xPEN

	### Predicts away team minor penalties
	for index in range(18):
		player=awayTeamRoster[index].replace("\n",'')
		playerPenalties=LinearRegression()
		try:
			stats=pd.read_csv("moneypuckPlayerStats/%s.csv" % (player))
		except:
			print("No stats for player %s, prediction cannot be made: Aborting" % player)
			quit()

		xPEN=calcxPenalties(stats, "AWAY", gameInfo)
		awayTeamXPEN=awayTeamXPEN+xPEN

	return homeTeamxPen, awayTeamxPen



def calcxPenalties(stats, homeOrAway, gameInfo):
	if homeOrAway=="HOME":
		opp=gameInfo['awayTeam']
		oppTeam='awayTeam'
	else:
		oppTeam='homeTeam'
		opp=gameInfo['homeTeam']

	stats=clean_df(stats, homeOrAway, gameInfo)

	statsAll=stats.drop(stats[stats.situation!="all"].index)
	avgTOI=statsAll['icetime'].sum()/statsAll.shape[0]
	daysSinceLastGame=str(gemeInfo['date']-int(statsAll.iloc[[-1]]["gameDate"]))
	playerPenalties.fit(statsAll[[gameInfo[oppTeam], homeOrAway, 'icetime', gameInfo['dayOfWeek'], "daysSinceLastGame_"+daysSinceLastGame]], statsAll['penalties'])

	if statsAll[gameInfo[oppTeam]].sum() == 0:
		oppCoef=0
	else:
		oppCoef=1
	if statsAll[homeOrAway].sum() == 0:
		H_A_coef=0
	else:
		H_A_coef=1
	if statsAll[gameInfo['dayOfWeek']].sum() == 0:
		DOW_coef=0
	else:
		DOW_coef=1	

	xPEN = playerPenalties.intercept_ + oppCoef*playerPenalties.coef_[0] + H_A_coef*playerPenalties.coef_[1] + avgTOI*playerPenalties.coef_[2] + DOW_coef*playerPenalties.coef_[3] + playerPenalties.coef_[4]
	if xPEN<0:
		xPEN=0.01
	return xPEN



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



def countDaysBetweenGamesMoneypuck(datesList):
	# This Function calculates and records the number of days since the last game
	# If the number is greater than 6, then it is recorded as 7
	# The most recent game gets a score of 0
	daysBetweenGamesList=[]
	i=0
	for index, date in datesList.iteritems():
		item=str(date)
		if i==0:
			daysBetweenGamesList.append(7)
			previousItem=item
			i=1
		else:
			# Calculates date of most recent game minus date of last game
			numberOfDaysSinceLastGame=(datetime.strptime(item,"%Y%m%d") - datetime.strptime(previousItem,"%Y%m%d")).days
			if numberOfDaysSinceLastGame==0:
				daysBetweenGamesList.append(daysBetweenGamesList[-1])
			elif numberOfDaysSinceLastGame<=7:
				daysBetweenGamesList.append(numberOfDaysSinceLastGame)
			elif numberOfDaysSinceLastGame>7:
				daysBetweenGamesList.append(7)
			if daysBetweenGamesList[-1]<0:
				print("Note: error in dataset. There are repeated games in player's stats")
				print(daysBetweenGamesList)
				print(datesList)

			previousItem=item

	return daysBetweenGamesList


def goalie_scoring_analysis_moneypuck():
	None


def player_even_strength_analysis_moneypuck():
	None

def player_PK_analysis_moneypuck():
	None
	




#gameCalculation('EDM', 'COL', 20220411, 2021, doRefAnalysis=False)
