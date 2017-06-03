# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from store.models import Beer
from django.shortcuts import render_to_response
from django.template import Template, Context

# Create your views here.

def shop(request, offset):
	beer_list = Beer.objects.all()
	a = open("/home/ihor/BeerShop/front-end/index.html")
	hl = Template(a.read())
	a.close()
	html = hl.render(Context({'beer_list': beer_list}))
	return HttpResponse(html)

def beer_page(request, offset):
	beer = Beer.objects.get(id = offset)
	a = open("/home/ihor/BeerShop/front-end/beerpage.html")
	hl = Template(a.read())
	a.close()
	html = hl.render(Context({'beer': beer}))
	return HttpResponse(html)