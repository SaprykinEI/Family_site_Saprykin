from django.urls import path
from gallery.views import AlbumListView  # Импорт только нужных представлений

app_name = 'gallery'

urlpatterns = [
    path('', AlbumListView.as_view(), name='album_list'),
    ]