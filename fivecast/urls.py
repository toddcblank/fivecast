from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^(?P<scheduleId>\d+)/$', views.showSchedule, name='showSchedule'),
    url(r'^(?P<scheduleId>\d+)/reschedule', views.rescheduleWork, name='rescheduleWork')
)