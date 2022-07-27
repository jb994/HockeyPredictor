#! /usr/bin/python

#import sys
import argparse
from Download.downloadTeamLines import downloadRoster
from Download.downloadPlayerStatsV2 import downloadTeamStats
from Process.V2_player_linear_regression import gameCalculation

parser = argparse.ArgumentParser()
parser.add_argument('homeTeam', type=str,
					help='homeTeam to Play')
parser.add_argument('awayTeam', type=str,
					help='awayTeam to Play')
parser.add_argument('--date', type=int) #yyyymmdd
parser.add_argument('--season', type=int) #yyyy
args = parser.parse_args()
keywordArgsDict = {
	'date':args.date,
	'season':args.season
}
print(args)
print(args.date)

#homeTeam = str(sys.argv[1])
#awayTeam = str(sys.argv[2])

downloadRoster(args.homeTeam)
downloadRoster(args.awayTeam)

gameCalculation(args.homeTeam, args.awayTeam, args.date, args.season)

