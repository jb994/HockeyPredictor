#! /usr/bin/python

import sys
import argparse
from ../Download.downloadTeamLines import downloadRoster
from hockey_predictor_experiment.Download.downloadPlayersStatsV2 import downloadTeamStats
from hockey_predictor_experiment.Process.V2_player_linear_regression import gameCalculation

parser = argparse.ArgumentParser()
parser.add_argument('--date') #yyyymmdd
parser.add_argument('--season') #yyyy
keywordArgs = parser.parse_args()
keywordArgsDict = {
	'date':args.date,
	'season':args.season
}
print(args.date)

homeTeam = str(sys.argv[1])
awayTeam = str(sys.argv[2])

downloadRoster(homeTeam)
downloadRoster(awayTeam)

gameCalculation(homeTeam, awayTeam, args.date, args.season)

