# download all player stats
# Want to download all player stats from 2010 on to just have in a big database

import urllib.request, urllib.parse, urllib.error
import os.path


def main():
	### Open the webpage with the catalogue of all players
	url_prefix="http://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/skaters/" #player_id.csv
	webPage=urllib.request.urlopen(url_prefix)
	directoryContent=webPage.read().decode()
	directoryContent=directoryContent.split("\n")
#	print(directoryContent)

	number_of_players=0
	line_number=0

	for index in range(1310, 10000):
		line=directoryContent[index]

#	for line in directoryContent:
		if line_number<11:
			None
		else:
			line=line.split('"')
			player_id_index=line.index("></td><td><a href=")+1
			player_id=line[player_id_index] # player_id is of form "1111111.csv"
			url=url_prefix+player_id
#			print(url)
			webPage=urllib.request.urlopen(url)
			webContent=webPage.read().decode()
			webContent_list=webContent.split("\n")
			player_name=webContent_list[1].split(',')[2]
			if os.path.isfile(('g2g_stats_moneypuck/%s.csv') % player_name):
				print("Player file for %s already exists" % player_name)
			else:
				print("Downloading player %s" % player_name)
				new_player_file=open("g2g_stats_moneypuck/" + player_name + '.csv', 'w+')
				new_player_file.write(webContent)
				new_player_file.close()

			number_of_players += 1

		line_number += 1

	print("Total number of players = %d" % number_of_players)


main()
