import os
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from content.models import Room



class Command(BaseCommand):

	'''
		Deletes rooms with more than 1 hour of life,
		also delethes theyr QR code image
	'''

	def handle(self, *args, **options):

		print 'Deleting rooms...'

		for room in Room.objects.all():
			try:
				if room.datetime < (timezone.now() + timedelta(hours=1)):

					# Delete the Qr code image
					os.system('rm /var/www/disrupt_flash_project/disrupt_flash/static/img/qr/%s.png' % room.slug)

					# Delete the room
					room.delete()

			except TypeError:
				pass  # Match hasnt started yet. (have to fix it?)


		print 'Rooms deleted ! ^_^'
