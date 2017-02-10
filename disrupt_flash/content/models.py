import qrcode

from django.db import models

from .functions import random_string



class Champion( models.Model ):

	id = models.CharField(max_length = 4, primary_key = True)
	img = models.CharField(max_length = 150, null = True, blank = True)
	key = models.CharField(max_length = 50, null = True, blank = True)
	name = models.CharField(max_length = 50, null = True, blank = True)

	def __unicode__(self):
		return self.name


class SummonerSpell( models.Model ):

	id = models.CharField(max_length = 4, primary_key = True)
	img = models.CharField(max_length = 150, null = True, blank = True)
	key = models.CharField(max_length = 50, null = True, blank = True)
	name = models.CharField(max_length = 50, null = True, blank = True)
	cooldown = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.name


class Region( models.Model ):

	name = models.CharField(max_length = 10, null = True, blank = True)

	def __unicode__(self):
		return self.name


class LolUser( models.Model ):

	id = models.CharField(max_length = 50, primary_key = True)
	name = models.CharField(max_length = 300, null = True, blank = True)
	region = models.ForeignKey( Region, null = True, blank = True )

	def __unicode__(self):
		return self.id


class Room( models.Model ):

	datetime = models.DateTimeField(auto_now_add=True, null=True)
	slug = models.SlugField(max_length = 70, default = '', editable = False, blank = True)
	summoner_id = models.CharField(max_length = 50, primary_key = True)
	summoner_cookie = models.CharField(max_length = 70, default = '', editable = False, blank = True)
	match_start = models.BooleanField(default = False)
	match_data = models.TextField(max_length = 40000, default = '', blank = True)
	qr = models.CharField(max_length = 200, default = '', blank = True)

	def __unicode__(self):
		return self.slug

	def save(self, *args, **kwargs):
		if self.slug == '':
			self.slug = random_string(10)
		if self.summoner_cookie == '':
			self.summoner_cookie = random_string(10)

		super(Room, self).save(*args, **kwargs)

