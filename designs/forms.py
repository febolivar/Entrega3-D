""" Form's module for designs app """

# Django

from django import forms

# Models

from designs.models import (
    Image,
    Project,
    State
)

from users.models import Enterprise

from PIL import Image as PImage
# Form classes

ALLOWED_UPLOAD_IMAGES = ('png', 'bmp', 'jpg', 'jpeg')

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image_original', 'image_processed', 'image_design')


class ProjectForm(forms.Form):
    """ Custom form to create or edit Projects """
    
    project_pk = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'readonly': None
            }
        )
    )

    project_name = forms.CharField(
        max_length = 50, 
        required = True,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    
    project_description = forms.CharField(
        max_length = 4000,
        required = False,
        widget = forms.Textarea(
            attrs = {
                'class' : 'form-control',
                'style' : 'resize: none;'
            }
        )
    )

    project_payment_value = forms.DecimalField(
        max_digits = 15,
        decimal_places = 2,
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control'
            }
        )
    )

    def clean_project_payment_value(self):
        """ Project payment validation """
        payment_value = self.cleaned_data['project_payment_value']
        
        if payment_value < 0:
            raise forms.ValidationError(
                {'project_payment_value': ["El valor pagado por el proyecto debe ser cero o mayor",]}
            )
        
        return payment_value


class EnterpriseForm(forms.Form):

    enterprise_name = forms.CharField(
        max_length = 150, 
        required = True,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    enterprise_email = forms.EmailField(
        max_length = 150,
        required = True,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    enterprise_url = forms.CharField(
        max_length = 200, 
        required = True,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    enterprise_initial_url = forms.CharField(
        max_length = 200, 
        required = True,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    
    def clean(self):
        url = self.cleaned_data['enterprise_url']
        o_url = self.cleaned_data['enterprise_initial_url']
        url_taken = Enterprise.objects.filter(enterprise_url = url).exists()

        if url_taken and not url == o_url:
            raise forms.ValidationError('Esta URL ya se encuentra en uso.')

        return url
    

class DesignUploadForm(forms.Form):
    
    designer_name = forms.CharField(
        max_length = 30, 
        required = False,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    designer_lastname = forms.CharField(
        max_length = 150, 
        required = False,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    designer_email = forms.EmailField(
        max_length = 150,
        required = False,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    design_name = forms.CharField(
        max_length = 50, 
        required = True,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    design_value = forms.DecimalField(
        max_digits = 15,
        decimal_places = 2,
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control'
            }
        )
    )

    design_project = forms.ModelChoiceField(
        queryset = Project.objects.all(),
        empty_label = None,
        widget=forms.Select(
            attrs = {
                'class':'form-control'
            }
        )
    )

    design_image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs = {
                'class':'form-control'
            }
        )
    )


    def __init__(self, *args, **kwargs):
        enterprise = kwargs.pop('enterprise', None)

        super(DesignUploadForm, self).__init__(*args, **kwargs)

        if enterprise:
            self.fields['design_project'].queryset = Project.objects.filter(project_enterprise = enterprise)


    def clean_design_image(self):
        image = self.cleaned_data['design_image']
        im = PImage.open(image)

        if im.format.lower() not in ALLOWED_UPLOAD_IMAGES:
            raise forms.ValidationError("Formato de imagen no admitido!")

        width, height = im.size

        if width < 800 and height < 600:
            raise forms.ValidationError("Sólo se permiten imágenes de 800x600 o más grandes!")

        image.seek(0)
        
        return image
        

