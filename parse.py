from __future__ import with_statement
from glob import glob
import argparse, re, os, sys
from bs4 import BeautifulSoup

import os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'webscrape.settings'
from scrape.models import *
from django.conf import settings

def main(args):
	"""Loop through all games an parse them."""
	if not os.path.isdir(args.dir):
		print "The specified folder is not a directory"
		sys.exit(1)

	NUMBER_OF_FILES = len(os.listdir(args.dir))
	if args.num_of_files:
		NUMBER_OF_FILES = args.num_of_files
	print "Parsing", NUMBER_OF_FILES, "files"
	sql = None
	
	# Skip his if not args.stdout because I am using Django sql mapping

	for i, file_name in enumerate(glob(os.path.join(args.dir, "*.html")), 1):
		with open(os.path.abspath(file_name)) as f:
			fileId = re.sub("[^0-9]","", file_name)
			parse_game(f,fileId)
			#contestants = parse_contestants(f, fileId)
			#earnings = parse_earnings(f, fileId)
	print "All done"

def parse_game(f, gid): # Don't need sql param because DJANGO
	"""Parses an entire Jeopardy! game and extrat individual clues."""
	bsoup = BeautifulSoup(f, "lxml")
	# the title is in the format:
	# J! Archive - Show #XXXX, aired 2004-09-16
	# the last part is all that is required
	airdate = bsoup.title.get_text().split()[-1]
	if not parse_round(bsoup, 1, gid, airdate) or not parse_round(bsoup, 2, gid, airdate):
		# one of the rounds does not exist
		pass
	# the final Jeopardy! round
	r = bsoup.find("table", clas_ = "final_round")
	if not r:
		# this game does not have a final clue
		return
	category = r.find("td", class_ = "category_name").get_text()
	text = r.find("td", class_ = "clue_text").get_text()
	answerDiv = BeautifulSoup(r.find("div", onmouseover = True).get("onmouseover"), "lxml")
	answer = answerDiv.find("em").get_text()
	#right = answerDiv.find("td").get_text()
	# False indicates no present value for a clue
	insert([gid, airdate, 3, category, False, text, answer, "False"])

def parse_round(bsoup, rnd, gid, airdate):
	"""Parses and inserts the list of clues from a whole round"""
	round_id = "jeopardy_round" if rnd == 1 else "double_jeopardy_round"
	r = bsoup.find(id = round_id)
	# the game may not have all the rounds
	if not r:
		return False
	# the list of categories for this round
	categories = [c.get_text() for c in r.find_all("td", class_ = "category_name")]
	# the x_coord determines which category a clue is in
	# because the categories come before the clues, we will
	# have to match them up with the clues later on
	x = 0
	for a in r.find_all("td", class_ = "clue"):
		if not a.get_text().strip():
			continue
		value = a.find("td", class_ = re.compile("clue_value")).get_text().lstrip("D: $")
		value = re.sub('[:$,]','',value)
		text = a.find("td", class_ = "clue_text").get_text()
		answerDiv = BeautifulSoup(a.find("div", onmouseover = True).get("onmouseover"), "lxml")
		answer = answerDiv.find("em", class_ = "correct_response").get_text()
		right = answerDiv.find("td", class_ = "right")
		if right == None:
			right = "Triple Stumper"
		else:
			right = right.get_text()
		insert([gid, airdate, rnd, categories[x], value, text, answer, right])
		x = 0 if x == 5 else x + 1
	return True

def parse_earnings(f, gid):
	airdate = AirDates.objects.get(game=gid)
	contestants = airdate.contestants.all()
	listDict = []
	for contestant in contestants:
		contestantDict = dict(player_id=contestant.id, player_nickname=contestant.player_nickname, round1=False, round2=False, round3=False)
		listDict.append(contestantDict)
	"""Scores at the end of rounds are not labeled with IDs"""
	# divs for scores "jeopardy_round" "double_jeopardy_round" "final_jeopardy_round"
	roundDict = {
		"round1": "jeopardy_round",
		"round2": "double_jeopardy_round",
		"round3": "final_jeopardy_round",
	}
	bsoup = BeautifulSoup(f, "lxml") 
	insertDict = []
	for k, r in roundDict.items():
		roundDiv = bsoup.find("div", id  = r)
		if not roundDiv:
			continue
		tables = roundDiv.find_all("table")
		t = int(-2) if r == "final_jeopardy_round" else int(-1)
		table = tables[t]
		tdList =  table.find_all("td")
		""" pair 0and3 1and4 2and5 """ 
		valList = []
		for td in tdList:
			val = re.sub('[:$,]','', td.get_text())	
			valList.append(val)
		insertDict = combine_td_and_contestants(listDict, valList, k)			
	
	for p in insertDict:
		n_earnings, created = Earnings.objects.get_or_create(round1=p['round1'], round2=p['round2'], round3=p['round3'], e_game_id=airdate.id, e_player_id=p['player_id'])	
	return True

def combine_td_and_contestants(playerDict, tdList,roundno):
	
	tdDict = {}
	if len(tdList) % 4 != 0:
		tdDict[tdList[0]] = int(tdList[3])
		tdDict[tdList[1]] = int(tdList[4])
		tdDict[tdList[2]] = int(tdList[5])
	else:
		tdDict[tdList[0]] = int(tdList[4])
		tdDict[tdList[1]] = int(tdList[5])
		tdDict[tdList[2]] = int(tdList[6])			
		tdDict[tdList[3]] = int(tdList[7])

	for k,v in tdDict.items():
		for player in playerDict:
			if k  == player['player_nickname']:
				player[roundno] = v
			else:
				continue
	return playerDict

def parse_contestants(f, gid):
	airdate, created = AirDates.objects.get_or_create(game=gid)
	bsoup = BeautifulSoup(f, "lxml")
	playerDiv = bsoup.find(id = "contestants_table")	
	ptags = playerDiv.find_all("p", class_ = "contestants")
	for p in ptags:
		playerLink = p.find("a")
		playerId = (playerLink.get('href')).split("=")[1]
		#playerId[1] is the player id
		playerName = playerLink.get_text()
		nickname = playerName.split(" ")[0]
		player, created = Contestants.objects.get_or_create(player_id=playerId, player_name=playerName, player_nickname=nickname)
		airdate.contestants.add(player)
	return True

def insert(clue):
	"""Inserts the given clue into the database"""
	# clue is [game, airdate, round, category, value, clue, answer, right]
	# note that at this point, clue[4] is Flase if round is 3
	# note that at this point, clue[7] is also false if round is 3	
	if "\\\'" in clue[6]:
		clue[6] = clue[6].replace("\\\'","'")
	if "\\\"" in clue[6]:
		clue[6] = clue[6].replace("\\\"","\"")

	airDate  = AirDates.objects.get(game=clue[0])
	airDate.airdate = clue[1]
	airDate.save()
	cat, created = Categories.objects.get_or_create(category=clue[3])
	documents, created = Documents.objects.get_or_create(clue=clue[5], answer=clue[6], right=clue[7])
	clues, created = Clues.objects.get_or_create(c_document_id=documents.id, c_game_id=airDate.id, c_round=clue[2], c_value=clue[4])
	classifications = Classifications.objects.get_or_create(clue_id_id=clues.id, category_id_id=cat.id)		

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description = "Parse games from the J! Archive Website.",
		add_help = False,
		usage = "%(prog)s [options]"
	)
	parser.add_argument(
		"-d", "--dir",
		dest = "dir",
		metavar = "<folder>",
		help = "The directory containing the game files",
		default = "j-archive"
	)
	parser.add_argument(
		"-n", "--number-of-files",
		dest = "num_of_files",
		metavar = "<number>",
		help = "The number of files to parse",
		type = int
	)
	parser.add_argument(
		"-f", "--filename",
		dest = "database",
		metavar = "<filename>",
		help = "the filename for the SQLLite database",
		default = "clues.db"
	)
	parser.add_argument(
		"--stdout",
		help = "output th clues to stdout and not a database",
		action = "store_true"
	)
	parser.add_argument("--help", action = "help", help = "shpw this help message and exit")
	parser.add_argument("--version", action = "version", version = "2014.06.05")
	main(parser.parse_args())
