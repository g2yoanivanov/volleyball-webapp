from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Tournament)
admin.site.register(Hall)
admin.site.register(Match)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Referee)
admin.site.register(Ticket)