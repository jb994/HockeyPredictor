#! /usr/bin/python
import os
### Deletes all the player files from a certain team

def main():
	#[['ANA','ARI','BOS','BUF','CAR','CBJ','CGY','CHI','COL','DAL','DET','EDM','FLA','L.A','MIN','MTL','N.J','NSH','NYI','NYR','OTT','PHI','PIT','S.J','STL','T.B','TOR','VAN','VGK','WPG','WSH']]
	team="T.B"
	delete_on=False

	### Opens the roster file for each team and checks that it exists.
	if delete_on:
		try:
			team_file=open("team_rosters/%s" % (team), 'r')
		except:
			print("Roster file for team %s could not be found: Aborting" % (team1))
			quit()

		for player in team_file.readlines():
			player=player.replace('\n','')
			os.remove("g2g_stats_moneypuck/%s.csv" % (player))
			print("Player %s deleted" % (player))

	else:
		print("To delete the player files please turn 'delete_on' to 'True'")



main()