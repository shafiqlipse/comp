from django.contrib import admin

# Register your models here.
from accounts.models import *
from dashboard.models import *
from netball.models import *
from football.models import *
from handball.models import *
from volleyball.models import *
from basketball3.models import *


# Register your models here.
admin.site.register(User)
admin.site.register(Sport)
admin.site.register(Championship)
admin.site.register(Season)
admin.site.register(School)
admin.site.register(Football)
admin.site.register(Netball)
admin.site.register(Handball)
admin.site.register(Volleyball)
admin.site.register(Basketball3)
