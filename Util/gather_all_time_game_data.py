# Create an all_time game file with every line
# being gameid, gameDate, H_team, A_team, player, player ,player, ...

import os
import pandas as pd


def main():


	print("Reading gameID csv file")
	all_game_ids=pd.read_csv("game_id_db.csv")

	all_game_ids.drop(all_game_ids[all_game_ids.situation!="all"].index, inplace=True)
#	all_game_ids.drop(all_game_ids[all_game_ids.situation!="HOME"].index, inplace=True)
	all_game_ids.drop(all_game_ids[all_game_ids.playoffGame!=0].index, inplace=True)

	### Create a column which gives the results of the game
	# ['goalsFor'] # ['goalsAgainst']
	all_game_ids['home_team_win']=(all_game_ids['goalsFor']>all_game_ids['goalsAgainst'])
#	all_game_ids.home_team_win=all_game_ids.home_team_win_bool.astype(int)



#	print(all_game_ids['gameId'])
	game_id_dict={}
	print("Initializing gameID dictionary")
	for index, row in all_game_ids.iterrows():
		### Creates a dictionary to organize each game and all the players who played that game
		### Will be used to write output file once finished.
		gameID=row["gameId"]
		if gameID not in game_id_dict.keys():
			if row['home_or_away'] == "HOME":
				home_team=row["playerTeam"]
				away_team=row["opposingTeam"]
				if row['goalsFor']>row['goalsAgainst']:
					game_winner="HOME"
				elif row['goalsAgainst']>row['goalsFor']:
					game_winner="AWAY"
				else:
					game_winner='NaN'

#			if row['goalsFor']>row['goalsAgainst']:
#				home_team_result='W'
#			elif row['goalsFor']<row['goalsAgainst']:
#				home_team_result='L'
#			else:
#				home_team_result='NaN'
			else:
				home_team=row["opposingTeam"]
				away_team=row["playerTeam"]
				if row['goalsAgainst']>row['goalsFor']:
					game_winner='HOME'
				elif row['goalsFor']>row['goalsAgainst']:
					game_winner='AWAY'
				else:
					game_winner='NaN'

			# Creates dictionary entry for that game with 
			# date, h_team, a_team, h_team_roster, a_team_roster, h_team_playerids, a_team_playerids
#			print(gameID)
			game_id_dict[str(gameID)]=[str(gameID), str(row["gameDate"]), home_team, away_team, [], [], [], [], game_winner]


	### For every player file in the directory, this iterates over every line
	### and or every game it determines if the player was playing home or away
	print("Iterating through player files")
#	print(os.listdir("g2g_stats_moneypuck"))
	for player_filename in os.listdir("g2g_stats_moneypuck"):
		if player_filename[0]!='.':
			player_file=open("g2g_stats_moneypuck/%s" % player_filename, 'r')
			player=os.path.splitext(player_filename)[0]
#			print(player)
			first_line_read=False

			for line in player_file.readlines():
				if first_line_read:
					line_list=line.split(',')
					if line_list[8]!='G':
						if line_list[9]=='all':
#							print(line_list[3])
							if line_list[6]=='HOME':
								if line_list[0] not in game_id_dict[str(line_list[3])][6]:
									game_id_dict[str(line_list[3])][4].append(player)
									game_id_dict[str(line_list[3])][6].append(line_list[0])
							else:
								if line_list[0] not in game_id_dict[str(line_list[3])][7]:
									game_id_dict[str(line_list[3])][5].append(player)
									game_id_dict[str(line_list[3])][7].append(line_list[0])

				else:
					first_line_read=True

			player_file.close()


	### Once every player file has been read then this is all written to an all_time
	### games roster file
	print("")
	print("Iterating through player files complete: beginning to write to output file")
	games_file=open("game_rosters_all_time.csv",'w+')
	games_file.write("gameid,gameDate,H_team,A_team,winner,hp1,hp2,hp3,hp4,hp5,hp6,hp7,hp8,hp9,hp10,hp11,hp12,hp13,hp14,hp15,hp16,hp17,hp18,ap1,ap2,ap3,ap4,ap5,ap6,ap7,ap8,ap9,ap10,ap11,ap12,ap13,ap14,ap15,ap16,ap17,ap18\n")
	problem_games_list=[]

	number_of_games_written=0
	for key, v in game_id_dict.items():

		if len(v[4]) != 18 or len(v[5]) !=18:
			problem_games_list.append([v[0], v[1], v[2], v[3]])
			print(key)
			print(v[4])
			print(v[5])
		else:
			string_to_write=",".join([v[0], v[1], v[2], v[3], v[8],','.join(v[4]), ','.join(v[5]),'\n'])
			games_file.write(string_to_write)

			number_of_games_written += 1


		if number_of_games_written%100==0 and number_of_games_written!=0:
			print("%d games written" % number_of_games_written)

	games_file.close()
	print("Writing Complete")

	if len(problem_games_list) != 0:
		print("%d problem games" % len(problem_games_list))
		for item in problem_games_list:
			print(item)







main()
