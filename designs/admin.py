""" Design's admins module """

# Django

from django.contrib import admin

# Models

from .models import (
    State,
    Design,
    Image,
    Project
)


# Register.

admin.site.register(State)
admin.site.register(Design)
admin.site.register(Image)
admin.site.register(Project)
