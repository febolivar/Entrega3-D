""" View's module for Design's Apps"""

# Django
from django.conf.global_settings import MEDIA_URL
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage

from ISIS4426_Grupo06_Proyecto1.settings import BASE_DIR
from designs.forms import ImageForm
from .models import Project, Design, Enterprise, Image, State
from designs.models_views import design_view
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from designs.queue import send_sqs_message

from designs.forms import (ProjectForm, EnterpriseForm, DesignUploadForm)

from django.db.models import Count
from django.contrib import messages
# Test
from PIL import Image as Image2
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    View
)

import boto

# Multiproppurse Home

def home(request):
    """ Basic information page """
    return render(request, 'designs/home_saas.html')


# Enterprise's Admin views

class EnterpriseListView(LoginRequiredMixin, ListView):
    """ Admin home page """
    template_name = 'designs/home_enterprise.html'
    paginate_by = 10

    def get_queryset(self):
        projectList = Project.objects.select_related('project_enterprise').filter(
            project_enterprise=Enterprise.objects.filter(user=self.request.user)[0]).order_by('-project_create_date')
        designListFinal = []
        for project in projectList:
            desingList = Design.objects.select_related('design_project').filter(design_project=project).order_by(
                '-design_create_date')
            for design in desingList:
                designListFinal.append([design,project.project_name])
        return designListFinal
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enterprise'] = Enterprise.objects.get(user_id = self.request.user)
        return context


class ShowDesignListView(ListView):
    """ Admin home page """
    template_name = 'designs/home_enterprise.html'
    paginate_by = 10

    def get_queryset(self):
        name = self.kwargs['urlempresa']
        projectList = Project.objects.select_related('project_enterprise').filter(
            project_enterprise=Enterprise.objects.filter(enterprise_url=name)[0]).order_by('-project_create_date')
        designList = []
        designListFinal = []
        onelist = [[], '']
        for project in projectList:
            onelist = [[], '']
            desingList = Design.objects.select_related('design_project').filter(design_project=project).order_by(
                '-design_create_date')
            for design in desingList:
                onelist[0] = design
                onelist[1] = project.project_name
                designListFinal.append(onelist)
        return designListFinal


@login_required
def view_projects(request):
    """ View projects page """
    print(request.user)
    if not request.user.is_staff:
        return redirect('home:home')
    return render(request, 'designs/view_projects.html')


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'designs/view_projects.html'
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.filter(project_enterprise=Enterprise.objects.filter(user=self.request.user)[0]).order_by(
            '-project_create_date')


class DesignListView(LoginRequiredMixin, ListView):
    template_name = 'designs/view_designs.html'
    paginate_by = 10

    def get_queryset(self):
        return Design.objects.filter(design_project=self.kwargs['id']).order_by('-design_create_date')


@login_required
def image(self, *args, **kwargs):
    id = kwargs['id']
    path = kwargs['path']
    image = Image.objects.get(image_design=Design.objects.get(id=id))
    originalImage = str(image.image_original)
    processedImage = str(image.image_processed)
    
    conn = boto.connect_s3(os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_SECRET_ACCESS_KEY'))
    bucket = conn.get_bucket(os.getenv('AWS_STORAGE_BUCKET_NAME'))
    
    
    if path == 'original':
        #fileRoute = 'media/' + originalImage
        #name = originalImage.split('/', 1)[1]
        #imageFile = image.image_original
        s3_file_path = bucket.get_key(originalImage)
    else:
        #fileRoute = 'media/' + processedImage
        #name = processedImage.split('/', 1)[1]
        #imageFile = image.image_processed
        s3_file_path = bucket.get_key(processedImage)
        #s3_file_path = bucket.get_key(originalImage)


    #extension = Image2.open(imageFile).format
    #fileName = name.split('.', 1)[0]
    #contentType = 'image/' + extension
    #attachment = 'attachment; filename=%s' + '.' + extension
    #im = Image2.open(fileRoute)  # any Image object should work
    #response = HttpResponse(content_type=contentType)
    #response['Content-Disposition'] = attachment % fileName
    #im.save(response, extension)
    #return response

    url = s3_file_path.generate_url(
            expires_in=600,
            response_headers={'response-content-disposition': 'attachment;',}
        ) # expiry time is in seconds

    return HttpResponseRedirect(url)


@login_required
def manage_projects(request):
    """ Manage projects page """
    if not request.user.is_staff:
        return redirect('home:home')

    enterprise = Enterprise.objects.get(user_id=request.user)
    projects = Project.objects.filter(project_enterprise_id=enterprise).order_by('-project_create_date')

    if request.method == 'POST':
        form = ProjectForm(
            initial={'project_enterprise_id': enterprise}
        )

        if 'create-button' in request.POST:
            try:
                data = {}

                data['project_pk'] = '0'
                data['project_name'] = request.POST['project_name']
                data['project_description'] = request.POST['project_description']
                data['project_payment_value'] = request.POST['project_payment_value']

                form = ProjectForm(data)

                if form.is_valid():
                    active_state = State.objects.get(state_type='Proyecto', state_description='Activo')
                    Project.objects.create(
                        project_name=data['project_name'],
                        project_description=data['project_description'],
                        project_payment_value=data['project_payment_value'],
                        project_enterprise_id=enterprise.id,
                        project_state_id=active_state.id
                    )

                    projects = Project.objects.filter(project_enterprise_id=enterprise).order_by('-project_create_date')

                    form = ProjectForm(
                        initial={'project_enterprise_id': enterprise}
                    )
            except ObjectDoesNotExist:
                form = ProjectForm(
                    initial={'project_pk': 'Error ocurrido durante la creación del proyecto, por favor reintente.'}
                )

        elif 'edit-button' in request.POST:
            try:
                project = Project.objects.get(pk=request.POST['project_pk'], project_enterprise_id=enterprise)

                data = {}

                data['project_pk'] = request.POST['project_pk']
                data['project_name'] = request.POST['project_name']
                data['project_description'] = request.POST['project_description']
                data['project_payment_value'] = request.POST['project_payment_value']

                form = ProjectForm(data)

                if form.is_valid():
                    project.project_name = request.POST['project_name']
                    project.project_description = request.POST['project_description']
                    project.project_payment_value = request.POST['project_payment_value']

                    project.save()

            except ObjectDoesNotExist:
                form = ProjectForm(
                    initial={'project_pk': 'Error ocurrido durante la actualización, por favor reintente.'}
                )
        elif 'delete-button' in request.POST:
            try:
                project = Project.objects.get(pk=request.POST['pk'], project_enterprise_id=enterprise)
                project.delete()
                form = ProjectForm(
                    initial={'project_enterprise_id': enterprise}
                )
            except:
                form = ProjectForm(
                    initial={'project_pk': 'Error ocurrido durante la eliminación del proyecto, por favor reintente.'}
                )
        else:

            form = ProjectForm(
                initial={'project_enterprise_id': enterprise}
            )

    else:

        form = ProjectForm(
            initial={'project_enterprise_id': enterprise}
        )

    context = {
        'projects': projects,
        'form': form
    }

    return render(request, 'designs/manage_projects.html', context=context)


@login_required
def manage_account(request):
    """ Manage Account page """
    if not request.user.is_staff:
        return redirect('home:home')

    enterprise = Enterprise.objects.get(user_id=request.user)

    if request.method == 'POST':
        data = {}

        data['enterprise_name'] = request.POST['enterprise_name']
        data['enterprise_email'] = request.POST['enterprise_email']
        data['enterprise_url'] = request.POST['enterprise_url']
        data['enterprise_initial_url'] = enterprise.enterprise_url
        print(data)
        form = EnterpriseForm(data)

        if form.is_valid():
           
            enterprise.enterprise_name = request.POST['enterprise_name']
            enterprise.enterprise_email = request.POST['enterprise_email']
            enterprise.enterprise_url = request.POST['enterprise_url']
                
            enterprise.save()

    else:
        form = EnterpriseForm(
            initial={
                'enterprise_name': enterprise.enterprise_name,
                'enterprise_email': enterprise.enterprise_email,
                'enterprise_url': enterprise.enterprise_url,
                'enterprise_initial_url': enterprise.enterprise_url
            }
        )
        
    context = {
        'form': form
    }

    return render(request, 'designs/manage_account.html', context = context)


# Designer's View


@login_required
def designer_home(request):
    """ Designer home page """
    if request.user.is_staff:
        return redirect('home:home')
    return render(request, 'designs/home_designer.html')


# fe.bolivar
# Carga la página de subir diseños, cargando las opciones de proyectos
@login_required
def load_upload(request):
    qs = Project.objects.all().order_by('project_name')

    return render(request, 'designs/upload_designs.html', {'view': qs})


# Any enterprise View
# fe.bolivar
# Dada una empresa en la URL de la invocación muestra sus proyectos
def enterprise_view(request, enterprise):
    """ An specific enterprise page """

    if request.method == "POST":

        data = {}

        data['designer_name'] = request.POST['designer_name']
        data['designer_lastname'] = request.POST['designer_lastname']
        data['designer_email'] = request.POST['designer_email']
        data['design_name'] = request.POST['design_name']
        data['design_value'] = request.POST['design_value']
        data['design_project'] = request.POST['design_project']
        data['design_image'] = request.FILES.get('design_image')

        form = DesignUploadForm(data, request.FILES)

        if form.is_valid():
            try:
                user = User.objects.filter(
                    first_name = request.POST['designer_name'],
                    last_name = request.POST['designer_lastname'],
                    email = request.POST['designer_email'],
                    is_staff = False)[0]
            except IndexError:
                data = {
                    'password': 'Password123',
                    'is_superuser': False,
                    'username': request.POST['designer_name'],
                    'first_name': request.POST['designer_name'],
                    'last_name': request.POST['designer_lastname'],
                    'email': request.POST['designer_email'],
                    'is_staff': False
                }    
                user = User.objects.create_user(**data)       
            
            design = Design.objects.create(
                design_requested_price = request.POST['design_value'],
                design_name = request.POST['design_name'],
                design_state = State.objects.get(state_type='Diseño', state_description='En Proceso'),
                design_project = Project.objects.get(pk =  request.POST['design_project']),
                design_creator = user
            )

            image = Image.objects.create(
                image_design = design,
                image_original= request.FILES.get('design_image')
            )

            image.save()

            # Send message to queue SQS
            send_sqs_message(str(image.pk))

            founded_enterprise = Enterprise.objects.get(enterprise_url=enterprise)
            form = DesignUploadForm(enterprise = founded_enterprise)
            messages.success(request, "PostGenerado!")
            return HttpResponseRedirect(request.path_info)

    try:

        founded_enterprise = Enterprise.objects.get(enterprise_url=enterprise)

        projects = Project.objects.filter(project_enterprise=founded_enterprise).order_by('-project_create_date')
        
        content = []
        
        for project in projects:
            designs = Design.objects.filter(design_project_id = project, design_state_id = 2).order_by('-design_create_date')
            designs_content = []
            for design in designs:
                images = Image.objects.filter(image_design_id = design)

                image = {
                    'design': design,
                    'image': images
                }
            
                designs_content.append(image)
                
            content.append (
                {
                    'project': project,
                    'designs': designs_content
                }
            )

        if request.method == "GET":
            form = DesignUploadForm(enterprise = founded_enterprise)
        
        context = {
            'enterprise': founded_enterprise,
            'content' : content,
            'form': form
        }
        
        return render(request, 'designs/enterprise_url.html', context = context )

    except ObjectDoesNotExist:
        return render(request, 'designs/error_404.html')


# fe.bolivar
# Dado un id de diseño, este se cargará y mostrará sus atributos
def show_design(request, design):
    print("id enviado: ")
    print(design)
    id_design = design
    qs = Design.objects.filter(id=id_design).first()

    dv = design_view()
    dv.id = qs.pk
    dv.create_date = qs.design_create_date.strftime('%Y-%m-%d %H:%M:%S')
    dv.requested_price = "$ " + str(qs.design_requested_price)
    dv.name = qs.design_name
    dv.state = qs.design_state.state_description
    dv.project = qs.design_project.project_name
    dv.project_description = qs.design_project.project_description
    dv.creator = qs.design_creator
    dsimg = Image.objects.filter(image_design_id=id_design).first()  # TODO: Mejorar esta consulta
    dv.image_original = settings.MEDIA_URL + str(dsimg.image_original)

    if str(dsimg.image_processed) != "":
        dv.image_processed = settings.MEDIA_URL + str(dsimg.image_processed)
    else:
        dv.image_processed = ""

    return render(request, 'designs/show_design.html', {'view': dv})


# fe.bolivar
# Guardar un diseño subido desde la página
def upload_design(request):
    # TODO: Validar tipo de imagen (png, bmp, jpg y/o jpeg)
    # TODO: Validar tamaño imagen, debe ser de mínimo 800x600 pixeles

    mensaje = ""
    print(request.method)
    print(request.FILES.get)
    print("get image")
    print(request.FILES.get('image_original'))

    if request.method == 'POST':  # and request.FILES.get('image_original'):
        design = Design(  # design_create_date=datetime.now(),
            design_name=request.POST.get('image'),
            design_requested_price=request.POST.get('requested_price'),
            design_state_id=1,  # En Proceso
            design_project=Project.objects.filter(id=request.POST.get('project')).first(),  # TODO: Mejorar consulta
            design_creator=request.user
        )

        url_redirect = ""
        print("Guardar diseño")
        design.save()

        data = {
            'image_original': request.FILES.get('image_original'),
            'image_processed': request.FILES.get('image_original'),
            'image_design': design,
        }

        form = ImageForm(data)
        print("Guardar imagen")

        imageg = Image(image_original=request.FILES.get('image_original'),
                       image_design=design
                       )
        imageg.save()

        print("Imagen guardada")
        mensaje = "OK"

        # Redirigir a página de diseños.
        # Según el proyecto que seleccionó, lo re-dirige al listado correspondiente
        proyecto_id = request.POST.get('project')
        #        return HttpResponseRedirect(reverse("designer_home", args=[proyecto_id]))
        # url = reverse('designer_home', kwargs={'slug': proyecto_id})
        # return HttpResponseRedirect(url)
        return HttpResponseRedirect('/designer_home/%s/' % proyecto_id)
    else:
        print("No post")
        mensaje = "NoPost"
    return render(request, 'designs/upload_designs_ok.html', {'view': mensaje})


def show_design_img(request, design):
    dsimg = Image.objects.filter(image_design_id=design).first()

    print("Imprime imagen:")
    print(dsimg.image_original)

    image_data = dsimg.image_original
    return HttpResponse(image_data, content_type="image/png")


@login_required
def designer_dashboard(request):
    """ Logged designers dashboard """
    
    designs_counter = Design.objects.filter(design_creator_id = request.user).count()
    designs_processed = Design.objects.filter(design_creator_id = request.user, design_state_id = 2).count()
    projects = Design.objects.filter(design_creator_id = request.user).values('design_project_id').distinct().count()
    
    context = {
        'designs' : designs_counter,
        'processed': designs_processed,
        'projects' : projects
    }
    
    return render(
        request = request,
        template_name = 'designs/home_designer.html',
        context = context
    )
