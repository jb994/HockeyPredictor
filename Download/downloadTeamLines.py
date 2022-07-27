#! /usr/bin/python


import urllib.request, urllib.parse, urllib.error
import os.path
from Download.downloadPlayerStatsV2 import downloadTeamStats

def downloadRoster(team):

	#[['ANA','ARI','BOS','BUF','CAR','CBJ','CGY','CHI','COL','DAL','DET','EDM','FLA','L.A','MIN','MTL','N.J','NSH','NYI','NYR','OTT','PHI','PIT','S.J','STL','T.B','TOR','VAN','VGK','WPG','WSH']]
	#team="EDM"
	minNumberOfGamesThreshold = 20 # Min number of games a player needs to have played to be able to use their stats

	print("Starting")
	teamNameDict={
		"ANA":"anaheim-ducks",
		"ARI":"arizona-coyotes",
		"BOS":"boston-bruins",
		"BUF":"buffalo-sabres",
		"CAR":"carolina-hurricanes",
		"CBJ":"columbus-blue-jackets",
		"CGY":"calgary-flames",
		"CHI":"chicago-blackhawks",
		"COL":"colorado-avalanche",
		"DAL":"dallas-stars",
		"DET":"detroit-red-wings",
		"EDM":"edmonton-oilers",
		"FLA":"florida-panthers",
		"L.A":"los-angeles-kings",
		"MIN":"minnesota-wild",
		"MTL":"montreal-canadiens",
		"N.J":"new-jersey-devils",
		"NSH":"nashville-predators",
		"NYI":"new-york-islanders",
		"NYR":"new-york-rangers",
		"OTT":"ottawa-senators",
		"PHI":"philadelphia-flyers",
		"PIT":"pittsburgh-penguins",
		"S.J":"san-jose-sharks",
		"STL":"st-louis-blues",
		"T.B":"tampa-bay-lightning",
		"TOR":"toronto-maple-leafs",
		"VAN":"vancouver-canucks",
		"VGK":"vegas-golden-knights",
		"WPG":"winnipeg-jets",
		"WSH":"washington-capitals"
	}

	if team not in teamNameDict:
		### Checks that user inputted a correct team code
		print("Team name is invalid: Aborting")
		quit()

	### URL to download the line combinations
	### Requests the lines from the website and opens the file

	urlForLines="http://www.dailyfaceoff.com/teams/" + teamNameDict[team] + "/line-combinations/"
	header = {
		'User-Agent':'Mozilla/5.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
	}
	req=urllib.request.Request(urlForLines, headers=header)
	webPage=urllib.request.urlopen(req)
	webContent=webPage.read().decode()
	webContentSplit=webContent.split('\n')

	### This gets the players currently in the lineup from the website
	newPlayerList, ppList, pkList, playerPositionDict, newGoalie = getNewPlayers(webContentSplit)

	### This gets the players in the old roster
	oldPlayerList, playerPositionDict, oldGoalie = getOldPlayers(team, playerPositionDict)

	### Chooses the final players to add to the new roster file
	finalPlayerList, newPlayerList, oldPlayerList = initializeFinalPlayers(newPlayerList, oldPlayerList)
	while len(finalPlayerList)<18:
		finalPlayerList, newPlayerList = whoToAddToRoster(finalPlayerList, newPlayerList, oldPlayerList, playerPositionDict, minNumberOfGamesThreshold)
	newGoalie = addGoalieToRoster(newGoalie, oldGoalie)


	writeSpecialTeams(team, ppList, pkList, finalPlayerList)
	newRosterFile=open("team_rosters/" + team, 'w+')
	for player in finalPlayerList:
		newRosterFile.write(player+'\n')
	newRosterFile.write(newGoalie+'\n')
	newRosterFile.close()

	print(finalPlayerList)
	print("Starting goalie is: " + newGoalie)

	downloadTeamStats(team)
	print("Finished Downloading Rosters and Players")



def getNewPlayers(webContentSplit):
	nextLineIsPlayer=False
	nextLineIsPpPlayer=False
	nextLineIsPkPlayer=False
	nextLineIsStartingGoalie=False
	newPlayerList=[]
	ppList=[]
	pkList=[]
	playerPositionDict={}
	positionList=["C1","C2","C3","C4","LW1","LW2","LW3","LW4","RW1","RW2","RW3","RW4","LD1","LD2","LD3","RD1","RD2","RD3"]
	ppPositionList=["PPC1","PPLW1","PPRW1","PPLD1","PPRD1"]
	pkPositionList=["PKC1", "PKC2", "PKLW1","PKLW2","PKRW1","PKRW2","PKLD1","PKLD2","PKRD1","PKRD2"]
	for line in webContentSplit:
		if nextLineIsPlayer==True:
			lineList=line.split('"')
			index=lineList.index(' alt=')
			player=lineList[index+1].replace("\n",'')
			newPlayerList.append(player)
			playerPositionDict[player]=playerPosition
			nextLineIsPlayer=False
		elif nextLineIsPpPlayer==True:
			lineList=line.split('"')
			index=lineList.index(' alt=')
			player=lineList[index+1].replace("\n",'')
			ppList.append(player)
			nextLineIsPpPlayer=False
		elif nextLineIsPkPlayer==True:
			lineList=line.split('"')
			index=lineList.index(' alt=')
			player=lineList[index+1].replace("\n",'')
			pkList.append(player)
			nextLineIsPkPlayer=False
		elif nextLineIsStartingGoalie==True:
			lineList=line.split('"')
			index=lineList.index(' alt=')
			goalie=lineList[index+1].replace("\n",'')
			nextLineIsStartingGoalie=False
		else:
			for position in positionList:
				if (line=='<td id="' + position + '">'):
					playerPosition=position
					nextLineIsPlayer=True
			for position in ppPositionList:
				if (line=='<td id="' + position + '">') or (line=='<td id="' + position + '" width="220">'):
					playerPosition=position
					nextLineIsPpPlayer=True
			for position in pkPositionList:
				if line=='<td id="' + position + '">':
					playerPosition=position
			if line=='<td id="G1">':
				nextLineIsStartingGoalie=True

	return newPlayerList, ppList, pkList, playerPositionDict, goalie



def getOldPlayers(team, playerPositionDict):
	oldPlayerList=[]
	oldRosterFileList=[]
	oldRosterFile=open("team_rosters/" + team, "r")
	oldRosterFilePlayerList=oldRosterFile.readlines()
	for index in range(18):
		oldRosterFileList.append(oldRosterFilePlayerList[index])
	if len(oldRosterFilePlayerList)==19:
		oldGoalie=oldRosterFilePlayerList[-1].replace("\n",'')
	else:
		oldGoalie=None
	for player in oldRosterFileList:
		player=player.replace('\n','')
		oldPlayerList.append(player)
		if player not in playerPositionDict:
			if oldRosterFileList.index(player+'\n')<12:
				playerPositionDict[player]='F'
			else:
				playerPositionDict[player]='D'
	oldRosterFile.close()

	return oldPlayerList, playerPositionDict, oldGoalie



def initializeFinalPlayers(newPlayerList, oldPlayerList):
	finalPlayerList=[]
	for player in newPlayerList:
		if player in oldPlayerList:
			finalPlayerList.append(player)
	for player in finalPlayerList:
		newPlayerList.remove(player)
		oldPlayerList.remove(player)
	newPlayerList=newPlayerList+oldPlayerList
	return finalPlayerList, newPlayerList, oldPlayerList



def whoToAddToRoster(finalPlayerList, newPlayerList, oldPlayerList, playerPositionDict, minGamesThreshold):
	print(finalPlayerList)
	for player in newPlayerList:
		if player in oldPlayerList:
			if os.path.isfile(('g2g_stats_moneypuck/%s.csv') % player):
				print('old: ' + player + ' (' + playerPositionDict[player] + ')')
			else:
				print('old: ' + player + ' (' + playerPositionDict[player] + '), (File not Found)')
		else:
			if os.path.isfile(('g2g_stats_moneypuck/%s.csv') % player):
				if len(open('g2g_stats_moneypuck/%s.csv' % player).readlines()) < minGamesThreshold*5-1:
					print('new: ' + player + ' (' + playerPositionDict[player] + '), (Under 20 GP)')
				else:
					print('new: ' + player + ' (' + playerPositionDict[player] + ')')
			else:
				print('new: ' + player + ' (' + playerPositionDict[player] + '), (File not Found)')

	playerToAdd=input("Which player should be added to roster? ")
	if playerToAdd in newPlayerList:
		newPlayerList.remove(playerToAdd)
		finalPlayerList.append(playerToAdd)
	elif playerToAdd=='other':
		playerToAdd=input("What other player should be added? ")
		finalPlayerList.append(playerToAdd)
	else:
		print("Incorrect Input")

	return finalPlayerList, newPlayerList



def addGoalieToRoster(newGoalie, oldGoalie):
	#if oldGoalie == newGoalie or oldGoalie==None:
	#	pass
	if (oldGoalie != newGoalie) and (oldGoalie is not None):
		goalieSelected=False
		while goalieSelected==False:
			if os.path.isfile(('g2g_stats_moneypuck/%s.csv') % oldGoalie):
				print('old: ' + oldGoalie + ' (G)')

			else:
				print('old: ' + oldGoalie + ' (G), (File not Found)')

			if os.path.isfile(('g2g_stats_moneypuck/%s.csv') % newGoalie):
				print('new: ' + newGoalie + ' (G)')

			else:
				print('new: ' + newGoalie + ' (G), (File not Found)')
			goalieToAdd=input("Which goalie should be added to roster? ")
			if goalieToAdd==oldGoalie or goalieToAdd==newGoalie:
				newGoalie=goalieToAdd
				goalieSelected=True
			else:
				print("Incorrect Input")
	return newGoalie



def writeSpecialTeams(team, ppList, pkList, finalPlayerList):
	ppRosterFile=open("team_rosters/pp_" + team, 'w+')
	pkRosterFile=open("team_rosters/pk_" + team, 'w+')
	for player in ppList:
		if player in finalPlayerList:
			ppRosterFile.write(player+'\n')
		else:
			print("\nPlayers in powerplay lines: " + str(ppList))
			print("Player in team roster: " + str(finalPlayerList))
			playerToAdd=''
			while playerToAdd not in finalPlayerList:
				playerToAdd=input('ERROR: player %s on powerplay is not in roster. Which Player should be added? ' % (player))
				if playerToAdd not in finalPlayerList:
					print("That player cannot be added")
			ppRosterFile.write(playerToAdd)
	for player in pkList:
		if player in finalPlayerList:
			print('Player %s added to PK' % player)
			pkRosterFile.write(player+'\n')
		else:
			print('ERROR: player %s on penalty kill is not in roster. Continuing' % (player))
	ppRosterFile.close()
	pkRosterFile.close()



#downloadRoster()
