""" User's forms """

# Django

from django import forms
from django.core.exceptions import ObjectDoesNotExist

# Models

from django.contrib.auth.models import User
from users.models import Enterprise

# Util
import re

class SignupForm(forms.Form):
    """ Custom form to sign up new users """

    # Fields

    username = forms.CharField( 
        max_length = 150, 
        required = True, 
        label = 'Empresa / Diseñador'
    )
    
    first_name = forms.CharField(
        max_length = 30, 
        required = True,
        label = 'Nombre'
    )
        
    last_name = forms.CharField(
        max_length = 150, 
        required = True,
        label= 'Apellido'
    )

    is_enterprise = forms.BooleanField(
        required = False,
        label = 'Empresa'
    )
    
    email = forms.EmailField(
        max_length = 150,
        required = True,
        label = 'Correo electrónico'
    ) 

    password = forms.CharField(
        max_length = 35, 
        required = True,
        label = 'Contraseña'
    )

    password_confirmation = forms.CharField(
        max_length = 35, 
        required = True,
        label = 'Confirmación de contraseña'
    )

    # Methods

    def clean_username(self):
        """ Method to validete if user exists """
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()

        if username_taken:
            raise forms.ValidationError('Este usuario ya se encuentra registrado.')
        
        return username
    

    def clean(self):
        """ Verify password confirmation match. """

        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError({'password': ["Las contraseñas no coinciden!",]})
        
        return data


    def save(self):
        """ Create a new user """
        data = self.cleaned_data
        if 'is_enterprise' in data:
            is_enterprise = data['is_enterprise']
            data['is_staff'] = is_enterprise

        data.pop('password_confirmation')
        data.pop('is_enterprise')

        user = User.objects.create_user(**data)
        if is_enterprise:
            enterprise = Enterprise(
                user = user,
                enterprise_name = data['username'],
                enterprise_email = data['email'],
                enterprise_url = ( data['username'] + str( user.pk ))
            )

            enterprise.save()