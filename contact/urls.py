from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, re_path
from contact import views


urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    # re_path(r'^.*\.html', views.gentella_html, name='gentella'),

    # path('', RedirectView.as_view(url="dashboard", permanent=False), name='index'),
    # path('dashboard', views.index, name='index'),
    # The home page
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('patients-list', views.patients_list, name='patients_list'),
    path('patients-form', views.patient_form, name='patients_form'),  
    path('update/<int:uid>', views.update_patient_status, name='update_patient_status'),
    path('edit/<int:uid>', views.edit, name='edit'),    
    path('delete/<int:uid>', views.delete_patient, name='delete_patient'), 
    path('add/', views.add_patients, name='add_patients'), 
    path('search', views.users, name='users'),
    path('results', views.search_results, name='search_results'),
]
