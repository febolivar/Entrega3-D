""" Design's module URL """

# Django
from django.urls import path

# Views
from designs import views
from .views import (
    ProjectListView,
    DesignListView,
    EnterpriseListView,
    ShowDesignListView
)

urlpatterns = [
    path(
        route = '',
        view = views.home,
        name = 'home'
    ),

    path(
        route = 'admin_home/',
        view = EnterpriseListView.as_view(),
        name = 'admin_home'
    ),  
    path(
        route = 'enterprise_home/<slug:urlempresa>',
        view = ShowDesignListView.as_view(),
        name = 'enterprise_home'
    ), 
    path(
        route = 'my_projects/',
        view = ProjectListView.as_view(),
        name = 'my_projects'
    ),

    path(
        route = 'manage_projects/',
        view = views.manage_projects,
        name = 'manage_projects'
    ),

    path(
        route = 'manage_account/',
        view = views.manage_account,
        name = 'manage_account'
    ),
    
    path(
        route = 'designer_home/<slug:id>/', 
        view = DesignListView.as_view(),
        name = 'designer_home'
    ),

    path(
        route = 'designer_dashboard/',
        view = views.designer_dashboard,
        name = 'designer_dashboard'
    ),

    path(
        route = 'download_original_design/<slug:path>/<int:id>',
        view = views.image,
        name = 'download_original_design'
    ),

    path(
        route = 'upload/',
        view = views.load_upload,
        name = 'load_upload'
    ),

    path(
        route = 'upload_design/',
        view = views.upload_design,
        name = 'upload_design'
    ),

    path(
        route = 'design/<int:design>',
        view = views.show_design,
        name = 'design'
    ),

    path(
        route = 'enterprise_design/<int:design>',
        view = views.show_design,
        name = 'enterprise_design'
    ),

    path(
        route = 'enterprise_design_img/<int:design>',
        view = views.show_design_img,
        name = 'enterprise_design_img'
    ),
]
