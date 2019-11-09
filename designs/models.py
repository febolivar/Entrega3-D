""" Design's application models """

# Django
from django.db import models

# Models from other applications
from users.models import Enterprise

# Native models
from django.contrib.auth.models import User

# Model's Section

class State(models.Model):
    """ State class to modeling states master """
    state_type = models.CharField(max_length = 20, null = False, blank = False, verbose_name = 'Tipo de Estado')
    state_description = models.CharField(max_length = 20, null = False, blank = False, verbose_name = 'Estado')
    state_order = models.IntegerField(null = False, blank = False, verbose_name = 'Orden de Estado')

    class Meta():
        """ State subclass to set meta information in States """
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'


    def __str__(self):
        """ ToString method from State Class """

        return ("{}".format(self.state_description))


class Project(models.Model):
    """ Project class to modeling projects """

    project_name = models.CharField(max_length = 50, null = False, blank = False, verbose_name = 'Nombre Proyecto')
    project_description = models.TextField(max_length = 4000, verbose_name = 'Descripción de Proyecto')
    project_payment_value = models.DecimalField(max_digits = 15, decimal_places = 2, verbose_name = 'Valor a Pagar')
    project_create_date = models.DateTimeField(auto_now_add = True, verbose_name = 'Fecha Creación')

    project_state = models.ForeignKey(State, on_delete = models.CASCADE, verbose_name = 'Estado del Proyecto')
    project_enterprise = models.ForeignKey(Enterprise, on_delete = models.CASCADE, verbose_name = 'Empresa')

    class Meta():
        """ Project subclass to set meta information in Projects """
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
    

    def __str__(self):
        """  ToString method from Project class """
        return (
            "{}".format(
                self.project_name
            )    
        )


class Design(models.Model):
    """ Design class to modeling designs """
    design_create_date = models.DateTimeField(auto_now_add = True, verbose_name = 'Fecha Creación')
    design_requested_price = models.DecimalField(max_digits = 15, decimal_places = 2, verbose_name = 'Valor Solicitado')
    design_name = models.CharField(max_length = 50, null = False, blank = False, verbose_name = 'Nombre del Diseño')

    design_state = models.ForeignKey(State, on_delete = models.CASCADE, verbose_name = 'Estado del Diseño')
    design_project = models.ForeignKey(Project, on_delete = models.CASCADE, verbose_name = 'Proyecto del Diseño')
    design_creator = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Diseñador')

    class Meta():
        """ Design subclass to set meta information in Desings """
        verbose_name = 'Diseño'
        verbose_name_plural = 'Diseños'


    def __str__(self):
        """  ToString method from Project class """
        return (
            "Design: {} -> Create Date: {} -> State: {} - By: {}".format(
                self.design_name,
                self.design_create_date.__str__(),
                self.design_state.__str__(),
                self.design_creator.__str__()
            )
        )


class Image(models.Model):
    """ Image class to modeling images """
    image_original = models.ImageField(upload_to = 'originals/', null = True, blank = True, verbose_name = 'Diseño Original')
    image_processed = models.ImageField(upload_to = 'processed/', null = True, blank = True, verbose_name = 'Diseño Procesado')

    image_design = models.OneToOneField(Design, on_delete = models.CASCADE)

    class Meta():
        """ Image subclass to set meta information in Images """
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imágenes'


    def __str__(self):
        """ ToString method from Image class """
        return (
            "{}".format(self.image_design.__str__())
        )
