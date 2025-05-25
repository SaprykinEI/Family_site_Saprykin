from django.urls import path
from family_tree.apps import FamilyTreeConfig

from family_tree.views import index_view, persons_list_view, person_create_view, person_detail_view


app_name = 'family_tree'

urlpatterns = [
    path('', index_view, name='index'),
    path('persons/', persons_list_view, name='persons'),
    path('persons/create/', person_create_view, name='person_create'),
    path('persons/detail/<int:pk>/', person_detail_view, name='person_detail'),


]