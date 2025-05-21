from django.urls import path
from family_tree.apps import FamilyTreeConfig

from family_tree.views import index

app_name = FamilyTreeConfig.name

urlpatterns = [
    path('', index, name='index'),
]