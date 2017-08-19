# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from store.models import Beer, Image, Comment
# Register your models here.


class BeerImageInline(admin.StackedInline):
	model = Image

class BeerCommentInline(admin.StackedInline):
	model = Comment
	extra = 3

class BeerAdmin(admin.ModelAdmin):
	list_display = ['title']
	inlines = [BeerCommentInline, BeerImageInline]

admin.site.register(Beer, BeerAdmin)