# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

#from django.conf import settings  

# Create your models here.

class Beer(models.Model):
	class Meta():
		db_table = 'beer'
	title = models.CharField(max_length = 150)
	description = models.TextField()
	price = models.FloatField()
	alcohol = models.FloatField()
	likes = models.IntegerField()
	dislikes = models.IntegerField()
	is_dark = models.BooleanField(default = True)
	is_filtered = models.BooleanField(default = True)

class Order(models.Model):
	class Meta():
		db_table = 'order'
	price = models.IntegerField()
	time = models.DateTimeField()
	user = models.ForeignKey(User, null = True)

class Gds(models.Model):
	class Meta():
		db_table = 'gds'
	beer = models.ForeignKey(Beer)
	amount = models.IntegerField()
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null = True)



class Comment(models.Model):
	class Meta():
		db_table = 'comment'
	text = models.TextField()
	beer = models.ForeignKey(Beer)
	user = models.ForeignKey(User, null = True)
