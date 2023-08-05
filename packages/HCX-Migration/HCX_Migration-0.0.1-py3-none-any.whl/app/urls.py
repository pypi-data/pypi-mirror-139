# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views,functions

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    re_path(r'check_for_duplicate_MG/*', functions.check_for_duplicate_MG, name='checkdup'),
    re_path(r'premigration/*', views.premigration, name='premigration'),
    re_path(r'postmigration/*', views.postmigration, name='postmigration'),
    path('compliance', views.compliance, name='compliance'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
