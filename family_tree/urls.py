from django.urls import path
from family_tree.apps import FamilyTreeConfig

from family_tree.views import IndexView, PersonsListView, PersonCreateView, PersonDetailView, PersonUpdateView, \
    PersonDeleteView, TreeView, TreeDataView, SpouseTreeDataView
app_name = 'family_tree'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('persons/', PersonsListView.as_view(), name='persons'),
    path('persons/create/', PersonCreateView.as_view(), name='person_create'),
    path('persons/detail/<slug:slug>/', PersonDetailView.as_view(), name='person_detail'),
    path('persons/update/<slug:slug>/', PersonUpdateView.as_view(), name='person_update'),
    path('persons/delete/<slug:slug>/', PersonDeleteView.as_view(), name='person_delete'),

    path('tree/', TreeView.as_view(), name='tree' ),
    path('tree/<int:person_id>/', TreeView.as_view(), name='tree_with_person'),
    path('tree/data/<int:person_id>/', TreeDataView.as_view(), name='tree_data'),
    path('tree/data/spouse/<int:spouse_id>/', SpouseTreeDataView.as_view(), name='spouse_tree_data'),
]
