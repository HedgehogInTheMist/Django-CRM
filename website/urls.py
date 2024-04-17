"""
Imports the path function from the django.urls module and all views from the current package.

The path function is utilized to define URL patterns associated with view functions for
a Django application.

views is a module that typically contains functions and classes representing the logic and rendering
of pages within the application. It is imported here to connect those view functions 
to their corresponding URL paths.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]
