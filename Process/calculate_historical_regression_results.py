### This file will use the results of the "gather_all_time_game_data.py" to run my regression
### program on every historical game available.

import pandas as pd
import player_linear_regression_for_iteration

def main():
	### This part opens the file with all the games and the rosters for each
	rosters_file=open("game_rosters_all_time.csv", 'r')
	previous_results_file=open("historical_game_regression_results.csv", 'r')
	roster_file_list=rosters_file.readlines()
	previous_results_file_list=previous_results_file.readlines()
	### Find the already completed games
	already_calculated_games_list=[]
	print("Reading all games already calculated")
	for line in previous_results_file_list:
		line_list=line.split(',')
		already_calculated_games_list.append(line_list[0].replace('\n',''))
	previous_results_file.close()
#	print(results_file_list)
	print("Starting Game Calculations")

#	first_line=True
	results_file=open("historical_game_regression_results.csv", 'w')
	for line in roster_file_list[1:]:
		line_list=line.split(',')
#		if first_line==True:
#			first_line=False
		if line_list[0] not in already_calculated_games_list and int(line_list[1])>=20100901:
			print(line_list[0])
			print(line_list[1])
			results=player_linear_regression_for_iteration.main(line_list)
			if results != False:
				difference1=results[0]-results[1]
				difference2=results[2]-results[3]
				difference3=results[4]-results[5]
				difference4=results[6]-results[7]
				team_to_win=0 # if positive home team wins, if negative away team wins
				if difference1>=0.1:
					team_to_win+= 1
				elif difference1<=-0.1:
					team_to_win+= -1
				if difference2>=0.1:
					team_to_win+= -1
				elif difference2<=-0.1:
					team_to_win+= 1
				if difference3>=0.1:
					team_to_win+= 1
				elif difference3<=-0.1:
					team_to_win+= -1
				if difference4>=0.1:
					team_to_win+= -1
				elif difference4<=-0.1:
					team_to_win+= 1			

	#############################
				if team_to_win==4:
					expected_winner="HOME"
					if line_list[4]=="HOME":
						prediction_result="Correct"
					else:
						prediction_result="Incorrect"

				elif team_to_win==3:
					expected_winner="HOME Probably"
					if line_list[4]=="HOME":
						prediction_result="Correct"
					else:
						prediction_result="Incorrect"

				elif team_to_win==-3:
					expected_winner="AWAY Probably"
					if line_list[4]=="AWAY":
						prediction_result="Correct"
					else:
						prediction_result="Incorrect"

				elif team_to_win==-4:
					expected_winner="AWAY"
					if line_list[4]=="AWAY":
						prediction_result="Correct"
					else:
						prediction_result="Incorrect"

				else:
					expected_winner="None"
					prediction_result="None"
	##############################
					
				list_to_write_list=line_list[:5]+list(map(str, results))
				list_to_write_list.extend([expected_winner, prediction_result])
				line_to_write=','.join(list_to_write_list) + '\n'
				print("Game %s completed" % (line_list[0]))
				results_file.write(line_to_write)
				results_file.flush()
			else:
				line_to_write=line_list[0] + '\n'
				results_file.write(line_to_write)
				print("Could not complete Analysis")
				results_file.flush()
			print("")

main()