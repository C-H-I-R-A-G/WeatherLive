from django.urls import path
from . import views
 
app_name = 'weather'

urlpatterns = [
    path('', views.index, name='index'),
    path('srch', views.srch, name='srch'),
]
