from django.core.management.base import BaseCommand, CommandError

from content.models import Region



class Command(BaseCommand):

	'''
		Creates all regions, so you dont have to type them
	'''

	def handle(self, *args, **options):

		print 'Creating regions...'

		regions = ['BR', 'EUNE', 'EUW', 'JP', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'PBE', 'RU', 'TR']

		for region in regions:
			new_region = Region()
			new_region.name = region
			new_region.save()

		print 'Regions created ! ^_^'