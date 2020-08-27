from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogin, name='index'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('batch/', views.batchView, name='batch'),
    path('project/', views.pjtView, name='project'),
    path('cbatch/', views.createBch, name='cbatch'),
    path('cproject/', views.createPjt, name='cproject'),
    path('gpl/', views.get_project_location, name='gpl'),
]