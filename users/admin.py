""" User's admin module """

# Django

from django.contrib import admin

# Models

from .models import Enterprise

# Mode Registry

admin.site.register(Enterprise)
