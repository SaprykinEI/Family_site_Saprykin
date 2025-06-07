from django.urls import path
from family_tree.apps import FamilyTreeConfig

from family_tree.views import index_view, persons_list_view, person_create_view, person_detail_view, person_update_view, \
    person_delete_view, tree_view, tree_data_view, spouse_tree_data
app_name = 'family_tree'

urlpatterns = [
    path('', index_view, name='index'),
    path('persons/', persons_list_view, name='persons'),
    path('persons/create/', person_create_view, name='person_create'),
    path('persons/detail/<int:pk>/', person_detail_view, name='person_detail'),
    path('persons/update/<int:pk>/', person_update_view, name='person_update'),
    path('persons/delete/<int:pk>/', person_delete_view, name='person_delete'),

    path('tree/', tree_view, name='tree' ),
    path('tree/data/<int:person_id>/', tree_data_view, name='tree_data'),
    path('tree/data/spouse/<int:spouse_id>/', spouse_tree_data, name='spouse_tree_data'),


]