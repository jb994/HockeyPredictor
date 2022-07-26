#! /usr/bin/python

### This program will download all the player g2g stats for a specific team
### as long as the players name is in the team roster file

import urllib.request, urllib.parse, urllib.error
from urllib.request import Request


def main(team1):
	#[['ANA','ARI','BOS','BUF','CAR','CBJ','CGY','CHI','COL','DAL','DET','EDM','FLA','L.A','MIN','MTL','N.J','NSH','NYI','NYR','OTT','PHI','PIT','S.J','STL','T.B','TOR','VAN','VGK','WPG','WSH']]
#	team1='VAN' # From codes above
#	team2='VGK' # From codes above
	list_of_failed_downloads=[]

	### Opens the roster file for each team and checks that it exists.
	try:
		team1_file=open("team_rosters/%s" % (team1), 'r')
	except:
		print("Roster file for team %s could not be found: Aborting" % (team1))
		quit()

	print("Overall team stats downloaded")
	url_for_team_stats="http://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/teams/" + team1 + ".csv" 
	req = Request(url_for_team_stats, headers={'User-Agent': 'Mozilla/5.0'})
	webPage=urllib.request.urlopen(req)
	webContent=webPage.read().decode()
	new_team_file=open("team_stats/" + team1 + '.csv', 'w+')
	new_team_file.write(webContent)
	new_team_file.close()


	for team in [team1_file]:
		player_list=team.readlines()
		for index in range(18):
			### Reads the player file already there to figure out the player's
			### ID number on moneypuck.com. This is then used to download the file
			player=player_list[index].replace("\n",'')
			try:
				downloadPlayerStats(player)
			except:
				list_of_failed_downloads.append(player)

	if len(player_list)==19:
		### This will get the goalie stats if he is in the roster file
		goalie=player_list[18].replace("\n",'')
		try:
			downloadPlayerStats(goalie, isGoalie=True)
		except:
			list_of_failed_downloads.append(goalie)

	print("")
	print("All stats downloaded: Finishing")
	team1_file.close()
	for player in list_of_failed_downloads:
		print("Could not find %s's player ID, you will need to manually download it from moneypuck.com" % (player))


def downloadPlayerStats(player, isGoalie=False):
	if not isGoalie:
		url_prefix="http://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/skaters/" #player_id.csv
	else:
		url_prefix="http://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/goalies/" #goalie_id.csv
	player_file=open("g2g_stats_moneypuck/" + player + '.csv', 'r')
	player_id=((player_file.readlines())[1].split(','))[0]

	url=url_prefix+player_id+'.csv'
	player_file.close()

	### Reads the player's stats from the webpage
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webPage=urllib.request.urlopen(req)
	webContent=webPage.read().decode()

	### Write the player's stats to a file on my computer
	new_player_file=open("g2g_stats_moneypuck/" + player + '.csv', 'w+')
	new_player_file.write(webContent)
	new_player_file.close()
	print("Stats for player %s downloaded" % (player))


main('CHI')
