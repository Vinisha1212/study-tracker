from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
  path('', views.dashboard, name='dashboard'),
    path('start/', views.start_study, name='start_study'),
    path('end/', views.end_study, name='end_study'),
    path('break/start/', views.start_break, name='start_break'),
    path('break/end/', views.end_break, name='end_break'),
    path('sessions/', views.session_list, name='session_list'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    
    

]
