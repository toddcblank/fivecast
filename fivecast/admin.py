from django.contrib import admin
from fivecast.models import Lane, Feature,Discipline,Schedule,DisiplineWorkForFeature,WorkBooked

admin.site.register(Lane)
admin.site.register(Discipline)
admin.site.register(Schedule)
admin.site.register(DisiplineWorkForFeature)
admin.site.register(WorkBooked)
admin.site.register(Feature)