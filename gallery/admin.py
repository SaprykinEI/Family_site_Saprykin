from django.contrib import admin

from gallery.models import Tag, Category, Album, Photo, Video


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'date', 'category')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('caption', 'date_taken', 'album')
    list_filter = ('album', 'date_taken', 'tags')
    search_fields = ('caption',)
    filter_horizontal = ('people', 'tags')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('caption', 'date_taken', 'album')
    list_filter = ('album', 'date_taken', 'tags')
    search_fields = ('caption',)
    filter_horizontal = ('people', 'tags')