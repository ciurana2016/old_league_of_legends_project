import ast
import json
import requests

from disrupt_flash.settings import API_KEY
from models import Region, LolUser, Room, Champion, SummonerSpell



def save_summoner(name, region):

	url = 'https://%s.api.pvp.net/api/lol/%s/v1.4/summoner/by-name/%s?api_key=%s' % (region.lower(),region.lower(), name, API_KEY)
	r = requests.get( url )

	if r.status_code == 403:
		return '403'

	n = r.json().keys()[0]
	summoner = LolUser()
	summoner.id = r.json()[n]['id']
	summoner.name = name
	
	real_region = Region.objects.get(name= region)
	summoner.region = real_region

	summoner.save()

	return summoner


def get_current_match(summoner_id):

	'''
		IMPORTANT --- hardcoded the platformids.
		There is no way to get this data from the lolAPI right now
		url to platformids = https://developer.riotgames.com/docs/regional-endpoints
	'''

	regions = {
		'BR' : 'BR1',
		'EUNE' : 'EUN1',
		'EUW' : 'EUW1',
		'JP' : 'JP1',
		'KR' : 'KR',
		'LAN' : 'LA1',
		'LAS' : 'LA2',
		'NA' : 'NA1',
		'OCE' : 'OC1',
		'TR' : 'TR1',
		'RU' : 'RU',
	}

	summoner = LolUser.objects.get(id= summoner_id)
	summoner_region = summoner.region.name
	platformid = ''

	for region, pid in regions.iteritems():
		if region == summoner_region:
			platformid = pid

	url = 'https://%s.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/%s/%s?api_key=%s' % (summoner_region.lower(), platformid, summoner.id, API_KEY )
	r = requests.get( url )

	if r.status_code == 404:
		return '404'

	return r.json()


def build_enemy_team(room_slug, want_string):
	'''
		Returns Json data of the enemy team, with the data the web will
		create the html and functionality
	'''
	room = Room.objects.get(slug= room_slug)
	
	if room.match_start == True:
		data = ast.literal_eval(room.match_data)
		return json.dumps(data, ensure_ascii=False)

	if room.match_data == '':
		data = get_current_match(room.summoner_id)
		if data == '404': return ''
	else:
		data = ast.literal_eval(room.match_data)

	# Find team contrary to our player
	player_team = 0

	for player in data['participants']:
		if player['summonerId'] == int(room.summoner_id):
			player_team = player['teamId']

	# Reloop to create enemy team
	enemy_team = {}

	for player in data['participants']:
		if player['teamId'] != player_team:

			# Look for mastery 'Insight' (reduces cooldown 15%) id=6241
			insight_mastery = False
			for mastery in player['masteries']:
				if mastery['masteryId'] == 6241:
					insight_mastery = True

			champion = Champion.objects.get(id= player['championId'])
			spell_1 = SummonerSpell.objects.get(id= player['spell1Id'])
			spell_2 = SummonerSpell.objects.get(id= player['spell2Id'])

			# Name exceptions
			champion_name = champion.name.replace("'","")
			champion_name = champion_name.replace(" ","")

			# New enemy
			enemy_team[player['championId']] = {
				'name' : champion_name,
				'spell_1' : {
					'name' : spell_1.name,
					'cd' : spell_1.cooldown,
					'id' : spell_1.id,
				},
				'spell_2' : {
					'name' : spell_2.name,
					'cd' : spell_2.cooldown,
					'id' : spell_2.id,
				},
				'insight_mastery' : insight_mastery,
			}

	room.match_start = True
	room.match_data = enemy_team
	room.save()

	if want_string:
		return json.dumps(enemy_team, ensure_ascii=False)
	else:
		return enemy_team











