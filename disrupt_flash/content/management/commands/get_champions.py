import json
import requests

from django.core.management.base import BaseCommand, CommandError
from disrupt_flash.settings import API_KEY

from content.models import Champion



class Command(BaseCommand):

	'''
		This gets all the champions and saves them, and theyr image.
		https://developer.riotgames.com/api/methods#!/1055/3633
	'''

	def handle(self, *args, **options):

		print 'Geting champions data...'
		
		request_url = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion?locale=en_US&champData=altimages&api_key=' + API_KEY
		r = requests.get( request_url )

		for name, champ in r.json()['data'].iteritems():

			print 'Getting ' + champ['name'] + ' ...'

			champion = Champion()
			champion.id = champ['id']
			champion.key = champ['key']
			champion.name = champ['name']

			img_url = 'http://ddragon.leagueoflegends.com/cdn/6.8.1/img/champion/%s.png' % champ['key']
			img_request = requests.get( img_url, stream=True )

			static_url = 'static/img/champion/%s.png' % champ['id']
			with open( static_url , 'wb') as f:
				for chunk in img_request:
					f.write(chunk)

			champion.img = static_url
			champion.save()
				
		print 'Done getting champions ^_^'
