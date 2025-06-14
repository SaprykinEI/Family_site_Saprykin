from django.urls import path

from gallery.views import AlbumListView, AlbumCreateView, FileUploadView, PhotoUploadPageView

app_name = 'gallery'

urlpatterns = [
    path('', AlbumListView.as_view(), name='album_list'),
    path('album/create/', AlbumCreateView.as_view(), name='album_create'),
    path('album/<int:album_id>/upload/', PhotoUploadPageView.as_view(), name='photo_upload'),  # страница загрузки
    path('album/<int:album_id>/upload/file/', FileUploadView.as_view(), name='file_upload'),  # API загрузки файлов
]