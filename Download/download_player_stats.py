#! /usr/bin/python

### This program will download all the player g2g stats for a specific team
### as long as the players name is in the team roster file

import urllib.request, urllib.parse, urllib.error

def main():
	#[['ANA','ARI','BOS','BUF','CAR','CBJ','CGY','CHI','COL','DAL','DET','EDM','FLA','L.A','MIN','MTL','N.J','NSH','NYI','NYR','OTT','PHI','PIT','S.J','STL','T.B','TOR','VAN','VGK','WPG','WSH']]
	team1='TOR' # From codes above
	team2='NYR' # From codes above
	list_of_failed_downloads=[]

	### Opens the roster file for each team and checks that it exists.
	try:
		team1_file=open("../team_rosters/%s" % (team1), 'r')
	except:
		print("Roster file for team %s could not be found: Aborting" % (team1))
		quit()
	try:
		team2_file=open("../team_rosters/%s" % (team2), 'r')
	except:
		print("Roster file for team %s could not be found: Aborting" % (team2))
		quit()


	url_prefix="http://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/skaters/" #player_id.csv
	goalie_url_prefix="http://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/goalies/" #goalie_id.csv
	for team in [team1_file, team2_file]:
		player_list=team.readlines()
		for index in range(18):
			### Reads the player file already there to figure out the player's
			### ID number on moneypuck.com. This is then used to download the file
			player=player_list[index].replace("\n",'')
			try:
				#print("g2g_stats_moneypuck/" + player + '.csv')
				player_file=open("../g2g_stats_moneypuck/" + player + '.csv', 'r')
				player_id=((player_file.readlines())[1].split(','))[0]
				url=url_prefix+player_id+'.csv'
				player_file.close()
				### Reads the player's stats from the webpage
			
				webPage=urllib.request.urlopen(url)
				webContent=webPage.read().decode()
				### Write the player's stats to a file on my computer
				new_player_file=open("../g2g_stats_moneypuck/" + player + '.csv', 'w+')
				new_player_file.write(webContent)
				new_player_file.close()
				print("Stats for player %s downloaded" % (player))
			except:
				list_of_failed_downloads.append(player)

		print("")

	if len(player_list)==19:
		### This will get the goalie stats if he is in the roster file
		goalie=player_list[18].replace("\n",'')
		try:
			player_file=open("../g2g_stats_moneypuck/" + goalie + '.csv', 'r')
			player_id=((player_file.readlines())[1].split(','))[0]
			url=goalie_url_prefix+player_id+'.csv'
			player_file.close()

			webPage=urllib.request.urlopen(url)
			webContent=webPage.read().decode()
			### Write the goalie stats into a file on my computer
			new_goalie_file=open('../g2g_stats_moneypuck/' + goalie + '.csv', 'w+')
			new_goalie_file.write(webContent)
			new_goalie_file.close()
			print("Stats for goalie %s downloaded" % (goalie))
		except:
			list_of_failed_downloads.append(goalie)


	print("All stats downloaded: Finishing")
	team1_file.close()
	team2_file.close()
	for player in list_of_failed_downloads:
		print("Could not find %s's player ID, you will need to manually download it from moneypuck.com" % (player))



main()