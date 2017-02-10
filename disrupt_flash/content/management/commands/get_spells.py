import json
import requests

from django.core.management.base import BaseCommand, CommandError
from disrupt_flash.settings import API_KEY

from content.models import SummonerSpell

from pprint import pprint

class Command(BaseCommand):

	'''
		This gets all the SUMMONER SPELLS and saves them, and theyr image.
		https://developer.riotgames.com/api/methods#!/1055/3634
	'''

	def handle(self, *args, **options):

		print 'Geting summoner spells data...'
		
		request_url = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/summoner-spell?spellData=all&api_key=' + API_KEY
		r = requests.get( request_url )

		for name, spell in r.json()['data'].iteritems():

			print 'Getting ' + spell['name'] + '...'

			new_spell = SummonerSpell()
			new_spell.id = spell['id']
			new_spell.key = spell['key']
			new_spell.name = spell['name']
			new_spell.cooldown = spell['cooldown'][0]

			img_url = 'http://ddragon.leagueoflegends.com/cdn/6.8.1/img/spell/' + spell['image']['full']
			img_request = requests.get( img_url, stream=True )

			static_url = 'static/img/spell/%s.png' % spell['id']
			with open( static_url , 'wb') as f:
				for chunk in img_request:
					f.write(chunk)			
			
			new_spell.img = static_url
			new_spell.save()
				
		print 'Done getting spells ^_^'
