from django.urls import path

from gallery.views import AlbumListView, AlbumCreateView, AlbumDetailView, FileUploadView, PhotoUploadPageView

app_name = 'gallery'

urlpatterns = [
    path('', AlbumListView.as_view(), name='album_list'),
    path('album/create/', AlbumCreateView.as_view(), name='album_create'),
    path('album/<int:pk>/upload/', PhotoUploadPageView.as_view(), name='photo_upload'),
    path('album/<int:pk>/upload/file/', FileUploadView.as_view(), name='file_upload'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
]