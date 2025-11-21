from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('application/create/', views.create_application, name='create_application'),
    #path('application/<int:application_id>/delete/', views.delete_application, name='delete_application'),
    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
    path('management/applications/', views.admin_applications, name='admin_applications'),
    path('management/application/<int:application_id>/change-status/', views.change_application_status, name='change_status'),
    path('management/categories/', views.manage_categories, name='manage_categories'),
    path('management/category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('application/<int:application_id>/delete/', views.delete_application, name='delete_application'),
]