# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render
from django.template import Template, Context, RequestContext
import math
from forms import *
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from store.models import *
from datetime import datetime


# Create your views here.
def shop(request, offset):
	check_ses(request)
	if 'is_dark' in request.GET:
		request.session['is_dark'] = int(request.GET['is_dark'])
	if 'is_filtered' in request.GET:
		request.session['is_filtered'] = int(request.GET['is_filtered'])
	beer_list_full = Beer.objects.all()

	if request.session['is_dark']!=2:
		beer_list_full = beer_list_full.filter(is_dark = request.session['is_dark'])

	if request.session['is_filtered']!=2:
		beer_list_full = beer_list_full.filter(is_filtered = request.session['is_filtered'])

	if offset == '':
		offset = 1
	beer_list = beer_list_full[20*int(offset)-20: 20*int(offset)]
	a = open("/home/ihor/BeerShop/front-end/index.html")
	hl = Template(a.read())
	a.close()
	count_of_pages = math.ceil(beer_list_full.count()/20)
	page_list = range(1, int(count_of_pages)+2)
	html = hl.render(Context({'beer_list': beer_list, 'range': page_list}))  
	return HttpResponse(html)


def beer_page(request, offset):
	print(request.session['backet'], request.session['is_dark'])
	#check_ses(request)
	beer = Beer.objects.get(id = offset)
	args = {}
	args['title'] = beer.title
	args['price'] = beer.price
	args['description'] = beer.description
	args['likes'] = beer.likes
	args['alcohol'] = beer.alcohol
	args['dislikes'] = beer.dislikes
	args['form'] = CommentForm
	args['buyform'] = BuyForm
	a = open("/home/ihor/BeerShop/front-end/beerpage.html")
	hl = Template(a.read())
	a.close()
	html = hl.render(Context({'args': args}))
	return HttpResponse(html)

def registration(request):
	check_ses(request)
	args = {}
	a = open("/home/ihor/BeerShop/front-end/reg.html")
	ht = Template(a.read())
	a.close()
	successful = ''
	args['form'] = UserForm
	html = ht.render(Context({'args': args}))	
	return HttpResponse(html)

def add_comment(request, beer_id):
	if request.POST:
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit = False)
			comment.beer = Beer.objects.get(id = beer_id)
			comment.save()	
	return redirect('/shop/beer%s/' % beer_id)

def done_reg(request):
	if request.POST:
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save()
	return redirect('/shop/1')

def check_ses(request):
	if 'initial' not in request.session:
		request.session['initial'] = True
		request.session['is_dark'] = 2
		request.session['is_filtered'] = 2
		request.session['backet'] = {}

def buy(request, beer_id):
	print('kek')
	if request.POST:
		ammount = request.POST['count']
		dick = {int(beer_id) : int(ammount)}
		tmp = request.session.get('backet')
		tmp.update(dick)
		request.session['backet'] = tmp
		print(request.session['backet'])
	return redirect('/shop/beer%s/' % beer_id)


def order(request):
	if True:
		order = Order(price = 0,
					  time = datetime.now(),
					  )
		order.save()
		price = 0
		backet = request.session['backet']
		for item_id, num in backet.items():
			print('aa')
			beer = Beer.objects.get(pk=int(item_id))
			price += beer.price*num
			n_gds = Gds(beer = beer, amount = num, order = order)
			n_gds.save()
		order.price = price
		order.save()
		return redirect('/shop/1')
	return redirect('/shop/login')

def test(request):
	check_ses(request)
	#beer = Beer.objects.get(id = offset)
	#test = request.session['backet'][0]
	a = open("/home/ihor/BeerShop/front-end/test.html")
	hl = Template(a.read())
	a.close()
	html = hl.render(Context({'test': test}))
	return HttpResponse(html)

def login_view(request):
	if request.POST:
		username = request.POST['username']
		password = request.POST['pass']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/shop/1')
		else:
			return redirect('/shop/login/')

