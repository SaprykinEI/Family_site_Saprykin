from django.urls import path

from gallery.views import (AlbumListView, AlbumCreateView, AlbumDetailView, FileUploadView, PhotoUploadPageView, \
    AlbumUpdateView, AlbumDeleteView, UserAlbumListView, PhotoUpdateCaptionView, PhotoDeleteView,
                           AlbumDeactivatedListView)

app_name = 'gallery'

urlpatterns = [
    path('', AlbumListView.as_view(), name='album_list'),
    path('album/deactivated', AlbumDeactivatedListView.as_view(), name='album_deactivated_list'),
    path('album/create/', AlbumCreateView.as_view(), name='album_create'),
    path('album/update/<int:pk>/', AlbumUpdateView.as_view(), name='album_update'),

    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
    path('album/<int:pk>/upload/', PhotoUploadPageView.as_view(), name='photo_upload'),
    path('album/<int:pk>/upload/file/', FileUploadView.as_view(), name='file_upload'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),

    path('my_albums/', UserAlbumListView.as_view(), name='user_albums'),

    path('photo/<int:pk>/update_caption/', PhotoUpdateCaptionView.as_view(), name='photo_update_caption'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),

]