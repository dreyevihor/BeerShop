
from django.template import Template, Context
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

def index(request):
	if 'initial' not in request.session:
		request.session['initial'] = True
		request.session['is_dark'] = 2
		request.session['is_filtered'] = 2
		request.session['backet'] = {}
	return redirect('/shop/')
