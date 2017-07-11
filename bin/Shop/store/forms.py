

from django.forms import ModelForm
from models import *
from django.contrib.auth.models import User

class CommentForm(ModelForm):
	class Meta():
		model = Comment
		fields = ['text']

class UserForm(ModelForm):
	class Meta():
		model = User
		fields = ['username', 'first_name', 'last_name', 'password']


class BuyForm(ModelForm):
	class Meta():
		model = Gds
		fields = ['amount']
	
class LoginForm(ModelForm):
	class Meta():
		model = User
		fields = ['username', 'password']