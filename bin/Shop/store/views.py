# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect, render
from django.template import Template, Context, RequestContext
import math
from forms import *
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from store.models import *
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import *


# Create your views here.
def shop(request, offset):
	try:
		offset = int(offset)
	except :
		raise Http404()	
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
	a = open("../../front-end/index.html")
	hl = Template(a.read())
	a.close()
	count_of_pages = math.ceil(beer_list_full.count()/20)
	page_list = range(1, int(count_of_pages)+2)
	html = hl.render(Context({'beer_list': beer_list, 'range': page_list}))  
	if request.user:
		print(request.user)
	return HttpResponse(html)


def beer_page(request, offset):
	print(request.session['backet'])
	check_ses(request)	
	beer = Beer.objects.get(id = offset)
	#try:
	#	beer = Beer.objects.get(id = offset)
	#except Beer.DoesNotExist:
	#	raise Http404("Poll does not exist")
	comments = Comment.objects.filter(beer = beer)
	args = {}
	args['title'] = beer.title
	args['price'] = beer.price
	args['description'] = beer.description
	args['likes'] = beer.likes
	args['alcohol'] = beer.alcohol
	args['dislikes'] = beer.dislikes
	args['form'] = CommentForm
	args['buyform'] = BuyForm
	args['comments'] = comments
	a = open("../../front-end/beerpage.html")
	hl = Template(a.read())
	a.close()
	html = hl.render(Context({'args': args}))
	return HttpResponse(html)

def registration(request):
	if not request.user.is_authenticated():
		check_ses(request)
		args = {}
		a = open("../../front-end/reg.html")
		ht = Template(a.read())
		a.close()
		args['form'] = UserCreationForm
		html = ht.render(Context({'args': args}))	
		return HttpResponse(html)
	return redirect('/shop/1')

def add_comment(request, beer_id):
	if request.POST:
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit = False)
			comment.beer = Beer.objects.get(id = beer_id)
			comment.user = request.user
			comment.save()	
	return redirect('/shop/beer%s/' % beer_id)

def done_reg(request):
	form = UserCreationForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			new_user = form.save()	
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
	order = Order(price = 0,
				  time = datetime.now(),
				  user_id = request.user.id,
				  )
	order.save()
	price = 0
	backet = request.session['backet']
	for item_id, num in backet.items():
		beer = Beer.objects.get(pk=int(item_id))
		price += beer.price*num
		n_gds = Gds(beer = beer, amount = num, order = order)
		n_gds.save()
		print(n_gds.beer.title)
	order.price = price
	print('a')
	#order.user = request.user
	print(order.user)
	print('b')
	order.save()
	print('c')
	return redirect('/shop/1')

def test(request):
	check_ses(request)
	#beer = Beer.objects.get(id = offset)
	#test = request.session['backet'][0]
	a = open("../../front-end/test.html")
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
			auth.login(request, user)
			return redirect('/shop/1')
		else:
			return redirect('/shop/login/')

def login(request):
	if not request.user.is_authenticated():
		check_ses(request)
		#beer = Beer.objects.get(id = offset)
		#test = request.session['backet'][0]
		a = open("../../front-end/login.html")
		hl = Template(a.read())
		a.close()
		html = hl.render(Context())
		return HttpResponse(html)
	return redirect('/shop/1')

def logout_view(request):
	auth.logout(request)
	return redirect('/shop/1')


def backet(request):
	backet = request.session['backet']
	check_list = []
	for beer_id, ammount in backet.items():
		tmp = {}
		tmp['beer_title'] = Beer.objects.get(id = beer_id).title
		tmp['beer_ammount'] = ammount
		tmp['price'] = ammount*Beer.objects.get(id = beer_id).price		
		check_list.append(tmp)
	html = open('../../front-end/backet.html')
	hl = Template(html.read())
	html.close()
	a = hl.render(Context({'check_list': check_list}))
	return HttpResponse(a)






