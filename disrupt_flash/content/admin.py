from django.contrib import admin

from .models import Champion, SummonerSpell, LolUser, Region, Room



admin.site.register( Champion )
admin.site.register( SummonerSpell )
admin.site.register( LolUser )
admin.site.register( Region )
admin.site.register( Room )