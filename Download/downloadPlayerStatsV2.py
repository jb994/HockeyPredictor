#! /usr/bin/python

### This program will download all the player g2g stats for a specific team
### as long as the players name is in the team roster file

import urllib.request, urllib.parse, urllib.error
from urllib.request import Request


def downloadTeamStats(team1):
	#[['ANA','ARI','BOS','BUF','CAR','CBJ','CGY','CHI','COL','DAL','DET','EDM','FLA','L.A','MIN','MTL','N.J','NSH','NYI','NYR','OTT','PHI','PIT','S.J','STL','T.B','TOR','VAN','VGK','WPG','WSH']]
#	team1='VAN' # From codes above
#	team2='VGK' # From codes above
	listOfFailedDownloads=[]

	### Opens the roster file for each team and checks that it exists.
	try:
		rosterFile=open("team_rosters/%s" % (team1), 'r')
	except:
		print("Roster file for team %s could not be found: Aborting" % (team1))
		quit()

	print("Overall team stats downloaded")
	urlForTeamStats="http://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/teams/" + team1 + ".csv" 
	req = Request(urlForTeamStats, headers={'User-Agent': 'Mozilla/5.0'})
	webPage=urllib.request.urlopen(req)
	webContent=webPage.read().decode()
	newTeamFile=open("team_stats/" + team1 + '.csv', 'w+')
	newTeamFile.write(webContent)
	newTeamFile.close()


	for team in [rosterFile]:
		playerList=team.readlines()
		for index in range(18):
			### Reads the player file already there to figure out the player's
			### ID number on moneypuck.com. This is then used to download the file
			player=playerList[index].replace("\n",'')
			try:
				downloadPlayerStats(player)
			except:
				listOfFailedDownloads.append(player)

	if len(playerList)==19:
		### This will get the goalie stats if he is in the roster file
		goalie=playerList[18].replace("\n",'')
		try:
			downloadPlayerStats(goalie, isGoalie=True)
		except:
			listOfFailedDownloads.append(goalie)

	print("")
	print("All stats downloaded: Finishing")
	rosterFile.close()
	for player in listOfFailedDownloads:
		print("Could not find %s's player ID, you will need to manually download it from moneypuck.com" % (player))


def downloadPlayerStats(player, isGoalie=False):
	if not isGoalie:
		urlPrefix="http://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/skaters/" #player_id.csv
	else:
		urlPrefix="http://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/goalies/" #goalie_id.csv
	playerFile=open("moneypuckPlayerStats/" + player + '.csv', 'r')
	playerID=((playerFile.readlines())[1].split(','))[0]

	url=urlPrefix+playerID+'.csv'
	playerFile.close()

	### Reads the player's stats from the webpage
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webPage=urllib.request.urlopen(req)
	webContent=webPage.read().decode()

	### Write the player's stats to a file on my computer
	newPlayerFile=open("moneypuckPlayerStats/" + player + '.csv', 'w+')
	newPlayerFile.write(webContent)
	newPlayerFile.close()
	print("Stats for player %s downloaded" % (player))


#downloadTeamStats('CHI')
