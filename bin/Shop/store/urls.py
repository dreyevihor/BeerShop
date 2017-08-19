from django.conf.urls import url, include
from store.views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^(\d*)$', shop),
    url(r'^beer(\d+)/comment$', csrf_exempt(add_comment)),
    url(r'^beer(\d+)/$', csrf_exempt(beer_page)),
    url(r'^registration/$', registration),
    url(r'^done_reg/$', done_reg),
    url(r'^beer(\d+)/buy$', csrf_exempt(buy)),
    url(r'^order/$', order),
    url(r'^test/$', test),
    url(r'^login_view/$', csrf_exempt(login_view)),
    url(r'^login/$', csrf_exempt(login)),
    url(r'^logout/$', logout_view),
    url(r'^backet/$', backet),
    url(r'^$', csrf_exempt(beer_page)),
]


