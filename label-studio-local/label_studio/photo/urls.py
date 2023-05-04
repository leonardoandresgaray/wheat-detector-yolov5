"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
from django.urls import include, path
from . import views

# TODO: these urlpatterns should be moved in core/urls with include('photo.urls')
urlpatterns = [
    path('photo/', views.simple_view, name='simple_view')
]
