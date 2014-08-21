'''
Created on 04/07/2014

@author: waldenilson
'''
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from TerraLegal import settings
from django.shortcuts import resolve_url
from django.utils.http import is_safe_url
from django.http.response import HttpResponseRedirect
from django.contrib.sites.models import get_current_site
from django.template.response import TemplateResponse


def login_form(request):
    
        # if the top login form has been posted
        if request.method == 'POST' and 'is_top_login_form' in request.POST:

            # validate the form
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():

                login(request, form.get_user())

                # if this is the logout page, then redirect to /
                # so we don't get logged out just after logging in
                if '/account/logout/' in request.get_full_path():
                    return HttpResponseRedirect('/')

        else:
            form = AuthenticationForm(request)    
    
        return {'login_form': form}


