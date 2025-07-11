from django.contrib import admin

from gallery.models import Tag, Category, Album, Photo, Video


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Административное представление для модели Tag """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Административное представление для модели Category. """
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """ Административное представление для модели Album.
        - автоматически заполнять поле 'slug' на основе 'title'."""
    list_display = ('pk', 'title', 'date', 'category')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """
        Административное представление для модели Photo.
        - для многих ко-многие полей 'people' и 'tags' добавляет удобный интерфейс с горизонтальными списками.
    """
    list_display = ('caption', 'date_taken', 'album')
    list_filter = ('album', 'date_taken', 'tags')
    search_fields = ('caption',)
    filter_horizontal = ('people', 'tags')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Административное представление для модели Video.
     - удобно выбирать связанные объекты 'people' и 'tags' через горизонтальный виджет."""
    list_display = ('caption', 'date_taken', 'album')
    list_filter = ('album', 'date_taken', 'tags')
    search_fields = ('caption',)
    filter_horizontal = ('people', 'tags')
