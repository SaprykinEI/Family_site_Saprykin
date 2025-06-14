from django.urls import path

from gallery.views import AlbumListView, AlbumCreateView, PhotoUploadView

app_name = 'gallery'

urlpatterns = [
    path('', AlbumListView.as_view(), name='album_list'),
    path('album/create/', AlbumCreateView.as_view(), name='album_create'),
    path('album/<int:album_id>/upload/', PhotoUploadView.as_view(), name='photo_upload'),
    ]