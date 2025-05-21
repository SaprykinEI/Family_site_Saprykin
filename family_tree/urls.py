from django.urls import path
from family_tree.apps import FamilyTreeConfig

from family_tree.views import index_view, persons_list_view
from . import views

app_name = FamilyTreeConfig.name

urlpatterns = [
    path('', views.index_view, name='index'),
    path('persons/', persons_list_view, name='persons'),
]