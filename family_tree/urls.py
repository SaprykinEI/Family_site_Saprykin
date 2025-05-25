from django.urls import path
from family_tree.apps import FamilyTreeConfig

from family_tree.views import index_view, persons_list_view, person_create_view
from . import views

app_name = 'family_tree'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('persons/', views.persons_list_view, name='persons'),
    path('persons/create/', views.person_create_view, name='person_create'),


]