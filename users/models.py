""" User's application models """

# Django
from django.db import models

# Native models
from django.contrib.auth.models import User


# Model's Section

class Enterprise(models.Model):
    """ Proxy class from User to add enterprise information
        to administrator """

    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True, verbose_name = 'Administrador')

    enterprise_name = models.CharField(max_length = 50, blank = False, verbose_name = 'Nombre empresa')
    enterprise_email = models.EmailField(max_length = 150, blank = False, verbose_name = 'Email empresa')
    enterprise_url = models.CharField(max_length = 100, blank = True, verbose_name = 'URL empresa')

    class Meta():
        """ Enterprise subclass to set meta information in Enterprise """
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'


    def __str__ (self):
        """ ToString method from Enterprise class """
        return ("{} -> URL: {} -> Email: {}"
            .format(self.enterprise_name, 
                self.enterprise_url, 
                self.enterprise_email))