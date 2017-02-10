import json
import qrcode
import requests


from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

from .models import LolUser, Region, Room
from disrupt_flash.settings import API_KEY
from .lol_api import save_summoner, get_current_match, build_enemy_team



class IndexView( TemplateView ):
	template_name = 'index.html'

class ContactView( TemplateView ):
	template_name = 'contact.html'

class SupportersView( TemplateView ):
	template_name = 'supporters.html'

class StartView( View ):

	'''
		Checks if we have the summoner on database, or requests it wit lol API
		Creates new room and gives the url to the user (automatically redirecting him with js)
		Gives a cookie to the user so ONLY he can delete the room
	'''

	def post(self, request):

		data = json.loads(request.body)

		# Check if we have the summoner on the database
		# if not we will add it
		try:
			summoner = LolUser.objects.get(name= data['name'], region__name= data['region'])
		except ObjectDoesNotExist:
			summoner = save_summoner(data['name'], data['region'])

			# If Summoner does not exist (most likely)
			if summoner == '403':
				return JsonResponse({'start':'403'})

		# Check if the summoner has created a Room already
		try:
			room = Room.objects.get(summoner_id= summoner.id)
			return JsonResponse({'start':'room_created'})
		except ObjectDoesNotExist:
			pass

		new_room = Room()
		new_room.summoner_id = summoner.id

		# Saves game data if it has started
		match = get_current_match( summoner.id )
		if get_current_match( summoner.id ) != '404':
			new_room.match_data = str(match)

		new_room.save()

		# Generate QR code
		q = 'static/img/qr/%s.png' % new_room.slug
		img = qrcode.make('%s/r/%s' % (request.META['HTTP_HOST'], new_room.slug))
		img.save(q)
		new_room.qr = q
		new_room.save()

		return JsonResponse({'start':new_room.slug, 'cookie':new_room.summoner_cookie})


class RoomView( DetailView ):
	model = Room
	template_name = 'room.html'

	def get_context_data(self, **kwargs):

		context = super(RoomView, self).get_context_data(**kwargs)

		context['enemy_team'] = build_enemy_team(context['room'].slug, True)

		# Config closeRoom
		can_close_room = self.request.COOKIES.get('close_room', '')

		if can_close_room == context['room'].summoner_cookie:
			context['can_close_room'] = True
		else:
			context['can_close_room'] = False


		print self.request.get_host
		
		return context


class BuildTeamView( View ):
	def get(self, request):
		room_slug =  request.GET.get('r', '')
		enemy_team = build_enemy_team(room_slug, False)
		return JsonResponse(enemy_team)


class CloseRoomView( View ):
	def get(self, request):

		try:
			close_room_cookie = self.request.COOKIES.get('close_room', '')

			room_to_close = Room.objects.get(summoner_cookie= close_room_cookie)
			room_to_close.delete()
		except ObjectDoesNotExist:
			pass

		return HttpResponseRedirect('/')






