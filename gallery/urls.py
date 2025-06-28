from django.urls import path

from gallery.views import (AlbumListView, AlbumCreateView, AlbumDetailView, FileUploadView, PhotoUploadPageView, \
    AlbumUpdateView, AlbumDeleteView, UserAlbumListView, PhotoUpdateCaptionView, PhotoDeleteView,
                           AlbumDeactivatedListView)

app_name = 'gallery'

urlpatterns = [
    path('', AlbumListView.as_view(), name='album_list'),
    path('album/deactivated', AlbumDeactivatedListView.as_view(), name='album_deactivated_list'),
    path('album/create/', AlbumCreateView.as_view(), name='album_create'),
    path('album/update/<slug:slug>/', AlbumUpdateView.as_view(), name='album_update'),

    path('album/<slug:slug>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
    path('album/<slug:slug>/upload/', PhotoUploadPageView.as_view(), name='photo_upload'),
    path('album/<slug:slug>/upload/file/', FileUploadView.as_view(), name='file_upload'),
    path('album/<slug:slug>/', AlbumDetailView.as_view(), name='album_detail'),

    path('my_albums/', UserAlbumListView.as_view(), name='user_albums'),

    path('photo/<int:pk>/update_caption/', PhotoUpdateCaptionView.as_view(), name='photo_update_caption'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),

]