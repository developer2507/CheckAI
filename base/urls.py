from django.urls import path
from . import views


urlpatterns = [
    path('', views.homePage, name='home'),
    
    path('check/', views.checkPage, name='check'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('panel/', views.panel, name='panel'),

    path('download/<int:file_id>/', views.download_file, name='download_file'),
]