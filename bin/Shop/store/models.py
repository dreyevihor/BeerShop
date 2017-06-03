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
	price = models.BigIntegerField()
	alcohol = models.FloatField()
	likes = models.IntegerField()
	dislikes = models.IntegerField()


class gds(models.Model):
	class Meta():
		db_table = 'gds'
	name = models.OneToOneField(Beer)
	amount = models.IntegerField()


class Order(models.Model):
	class Meta():
		db_table = 'order'
	gds = models.ForeignKey(gds)
	price = models.IntegerField()
	time = models.DateTimeField()
	user = models.OneToOneField(User, null = True)

