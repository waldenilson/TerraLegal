'''
Created on 04/07/2014

@author: waldenilson
'''
from django.contrib.auth.forms import AuthenticationForm

def login_form(request):
    form = AuthenticationForm()
    return {'login_form': form}