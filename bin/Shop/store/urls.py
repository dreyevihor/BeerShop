from django.conf.urls import url, include
from store.views import shop, beer_page
urlpatterns = [
    url(r'^(\d+)/', shop),
    url(r'^beer(\d+)/', beer_page)
]
