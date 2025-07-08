import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, ListView, CreateView, View, DetailView, UpdateView, DeleteView
from django.db.models import Q
from django.db.models.functions import ExtractYear

from rest_framework.reverse import reverse_lazy

from gallery.models import Album, Category, Tag, Photo, Video, AlbumLike
from gallery.forms import AlbumCreateForm, PhotoUploadForm


from family_tree.models import Person

from users.models import UserRoles, User
from .utils import convert_photo_to_webp


class UserAlbumListView(LoginRequiredMixin, ListView):
    """ Представление для отображения списка альбомов конкретного пользователя. """
    model = Album
    template_name = 'gallery/albums_user.html'
    context_object_name = 'albums'

    def get_queryset(self):
        """ Возвращает список альбомов, которые принадлежат текущему пользователю
        и которые активны (то есть показываются). """
        user = self.request.user
        return Album.objects.filter(
            owner=user,
            is_active=True
        ).select_related('category').prefetch_related(
            'photos__tags', 'photos__people', 'videos__tags', 'videos__people'
        ).order_by('-created_at').distinct()

    def get_context_data(self, **kwargs):
        """ Формирует контекст (данные), которые будут переданы в шаблон """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['view_mode'] = 'active'
        context['is_admin'] = user.role == UserRoles.ADMIN
        context['is_moderator'] = user.role == UserRoles.MODERATOR

        return context


class UserAlbumDeactivatedListView(LoginRequiredMixin, ListView):
    """ Представление для отображения списка неактивных альбомов конкретного пользователя. """
    model = Album
    template_name = 'gallery/albums_user.html'
    context_object_name = 'albums'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user

        qs = Album.objects.filter(owner=user, is_active=False).select_related('category').prefetch_related(
            'photos__tags', 'photos__people', 'videos__tags', 'videos__people'
        ).distinct()

        if user.role == UserRoles.ADMIN:
            return qs.order_by('-created_at')
        elif user.role == UserRoles.MODERATOR:
            return qs.order_by('-created_at')
        else:
            return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        """ Добавляет в контекст данные о роли пользователя """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['view_mode'] = 'inactive'
        context['is_admin'] = user.role == UserRoles.ADMIN
        context['is_moderator'] = user.role == UserRoles.MODERATOR

        return context


class AlbumListView(LoginRequiredMixin, ListView):
    """ Представление для отображения общего списка альбомов с фильтрами. """
    model = Album
    template_name = 'gallery/albums_list.html'
    context_object_name = 'albums'
    paginate_by = 12

    def get_queryset(self):
        """ Возвращает отфильтрованный QuerySet альбомов.
        Фильтрует по параметрам в GET-запросе: """
        user = self.request.user

        # Все активные альбомы
        qs = Album.objects.filter(is_active=True).select_related('category').prefetch_related(
            'photos__tags', 'photos__people', 'videos__tags', 'videos__people'
        ).distinct()

        # Фильтры GET
        category_ids = self.request.GET.getlist('category')
        years = self.request.GET.getlist('year')
        tag_ids = self.request.GET.getlist('tag')
        person_id = self.request.GET.get('person')
        search = self.request.GET.get('search', '').strip()

        if category_ids:
            qs = qs.filter(category__id__in=category_ids)

        if years:
            years_int = [int(y) for y in years if y.isdigit()]
            if years_int:
                qs = qs.annotate(year=ExtractYear('date')).filter(year__in=years_int)

        if tag_ids:
            qs = qs.filter(tags__id__in=tag_ids)

        if person_id and person_id.isdigit():
            qs = qs.filter(
                Q(photos__people__id=person_id) | Q(videos__people__id=person_id)
            )

        if search:
            qs = qs.filter(title__icontains=search)

        return qs.distinct().order_by('-created_at')

    def get_context_data(self, **kwargs):
        """
            Добавляет данные для шаблона:
            - Списки всех категорий, годов, тегов, людей
            - Выбранные пользователем фильтры
            - Флаги ролей пользователя (admin, moderator)
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['view_mode'] = 'active'

        context['categories'] = Category.objects.all()
        context['years'] = Album.objects.dates('date', 'year', order='DESC')
        context['tags'] = Tag.objects.all()
        context['persons'] = Person.objects.all()

        def safe_int_list(param_list):
            return [int(x) for x in param_list if x.isdigit()]

        context['selected_categories'] = safe_int_list(self.request.GET.getlist('category'))
        context['selected_years'] = safe_int_list(self.request.GET.getlist('year'))
        context['selected_tags'] = safe_int_list(self.request.GET.getlist('tag'))
        context['selected_persons'] = safe_int_list(self.request.GET.getlist('person'))
        context['search'] = self.request.GET.get('search', '')

        context['is_admin'] = user.role == UserRoles.ADMIN
        context['is_moderator'] = user.role == UserRoles.MODERATOR

        return context


class AlbumDeactivatedListView(LoginRequiredMixin, ListView):
    """ Представление для отображения списка деактивированных (неактивных) альбомов. """
    model = Album
    template_name = 'gallery/albums_list.html'
    context_object_name = 'albums'
    paginate_by = 12

    def get_queryset(self):
        """ Возвращает QuerySet неактивных альбомов с учетом роли пользователя. """
        user = self.request.user

        qs = Album.objects.filter(is_active=False).select_related('category').prefetch_related(
            'photos__tags', 'photos__people', 'videos__tags', 'videos__people'
        ).distinct()

        if user.role == UserRoles.ADMIN:
            # админ видит все неактивные
            return qs.order_by('-created_at')
        elif user.role == UserRoles.MODERATOR:
            # модератор — только свои
            return qs.filter(owner=user).order_by('-created_at')
        else:
            # юзер — пусто
            return Album.objects.none()

    def get_context_data(self, **kwargs):
        """ Добавляет данные о режиме просмотра и роли пользователя в контекст шаблона. """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['view_mode'] = 'inactive'
        context['is_admin'] = user.role == UserRoles.ADMIN
        context['is_moderator'] = user.role == UserRoles.MODERATOR

        return context


class AlbumCreateView(LoginRequiredMixin, CreateView):
    """Класс создания альбома"""
    model = Album
    form_class = AlbumCreateForm
    template_name = 'gallery/album_create.html'

    def get_queryset(self):
        """ Переопределяем метод, проверяем доступ пользователей"""
        user = self.request.user
        if user.role not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            raise PermissionDenied("У вас нет прав для создания альбома.")
        return super().get_queryset()

    def form_valid(self, form):
        """ Метод для автоматического присвоения создателя альбому """
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """ Переопределяем ссылку на которую будет переход после успешного создания альбома """
        return reverse_lazy('gallery:photo_upload', kwargs={'slug': self.object.slug})


class AlbumDetailView(LoginRequiredMixin, DetailView):
    """ Представление для детального просмотра одного альбома. Пользователь должен быть авторизован. """
    model = Album
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'gallery/album_detail.html'
    context_object_name = 'album'

    def get_object(self, queryset=None):
        """ Метод увеличение счётчика просмотров, если альбом просматривает не владелец """
        object = super().get_object(queryset)
        if self.request.user != object.owner:
            object.increment_view_count()
        return object

    def get_context_data(self, **kwargs):
        """ добавление данных в контекст шаблона """
        context = super().get_context_data(**kwargs)
        album = self.object

        context['videos'] = album.videos.all()
        context['previous_album'] = Album.objects.filter(pk__lt=album.pk).order_by('-pk').first()
        context['next_album'] = Album.objects.filter(pk__gt=album.pk).order_by('-pk').first()
        people_on_photos = Person.objects.filter(photos__album=album).distinct()
        context['people_on_photos'] = people_on_photos
        context['all_people'] = Person.objects.all().order_by('last_name', 'first_name')
        context['user_liked'] = AlbumLike.objects.filter(album=album, user=self.request.user).exists()
        context['likes_count'] = album.likes.count()
        liked_users = User.objects.filter(albumlike__album=album).distinct()
        context['liked_users'] = liked_users

        return context


class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    """ Представление для редактирования альбома. Требуется аутентификация пользователя. """
    model = Album
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    form_class = AlbumCreateForm
    template_name = 'gallery/album_update.html'
    success_url = reverse_lazy('gallery:album_list')

    def get_queryset(self):
        """Ограничиваем доступ к обновлению альбомов"""
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == UserRoles.ADMIN:
            return queryset
        elif user.role == UserRoles.MODERATOR:
            return queryset.filter(owner=user)
        return queryset.none()


    def get_initial(self):
        """Обеспечиваем правильный формат даты для input type='date'"""
        initial = super().get_initial()
        album = self.get_object()
        if album.date:
            initial['date'] = album.date.strftime('%Y-%m-%d')
        return initial



class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    """ Представление для удаления альбома. Требуется аутентификация пользователя. """
    model = Album
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'gallery/album_delete.html'
    success_url = reverse_lazy('gallery:album_list')

    def get_queryset(self):
        """Ограничиваем доступ к удалению альбомов"""
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == UserRoles.ADMIN:
            return queryset
        elif user.role == UserRoles.MODERATOR:
            return queryset.filter(owner=user)
        return queryset.none()


class PhotoUploadPageView(LoginRequiredMixin, View):
    """Отображает страницу загрузки медиа в альбом"""
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """Формируем queryset альбомов, к которым есть доступ для загрузки"""
        user = self.request.user

        if user.role == UserRoles.ADMIN:
            return Album.objects.all()
        elif user.role == UserRoles.MODERATOR:
            return Album.objects.filter(owner=user)
        return Album.objects.none()

    def get(self, request, slug):
        queryset = self.get_queryset()
        album = get_object_or_404(queryset, slug=slug)
        return render(request, 'gallery/photo_upload.html', {'album': album})



@method_decorator(login_required, name='dispatch')
class AlbumToggleLikeView(View):
    """ Представление для AJAX-переключения лайка на альбоме.
    Требует авторизации (login_required применяется к dispatch). """

    def post(self, request, *args, **kwargs):
        """ Получает слаг альбома из URL.
            - Проверяет наличие альбома по слагу.
            - Если лайк уже существует — удаляет его (снимает лайк).
            - Если лайка нет — создает его (ставит лайк).
            - Возвращает JSON-ответ с результатом:"""
        album_slug = kwargs.get('slug')
        user = request.user
        try:
            album = Album.objects.get(slug=album_slug)
        except Album.DoesNotExist:
            return JsonResponse({'error': 'Альбом не найден'}, status=404)

        like, created = AlbumLike.objects.get_or_create(album=album, user=user)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        like_count = album.likes.count()

        return JsonResponse({
            'liked': liked,
            'like_count': like_count
        })


@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(LoginRequiredMixin, View):
    """ Класс загрузки контента в альбом """
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """ Метод проверяет роль и возвращает список альбомов, доступных этому юзеру. """
        user = self.request.user

        if user.role == UserRoles.ADMIN:
            return Album.objects.all()
        elif user.role == UserRoles.MODERATOR:
            return Album.objects.filter(owner=user)
        return Album.objects.none()

    def post(self, request, slug):
        """ Обрабатывает загрузку файла (фото или видео) в альбом. """
        album = get_object_or_404(Album, slug=slug)
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return JsonResponse({'status': 'error', 'message': 'Файл не передан'}, status=400)

        content_type = uploaded_file.content_type

        if content_type.startswith('image/'):
            photo = Photo.objects.create(
                album=album,
                image=uploaded_file,
            )
            # Конвертация загруженного фото в WebP
            convert_photo_to_webp(photo)

            return JsonResponse({
                'status': 'ok',
                'type': 'photo',
                'id': photo.id,
                'filename': photo.image.name,
            })

        elif content_type.startswith('video/'):
            video = Video.objects.create(
                album=album,
                file=uploaded_file,
            )
            return JsonResponse({
                'status': 'ok',
                'type': 'video',
                'id': video.id,
                'filename': video.file.name,
            })

        return JsonResponse({'status': 'error', 'message': 'Неподдерживаемый тип файла'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PhotoUpdateCaptionView(LoginRequiredMixin, View):
    """ Класс обновляет подпись (caption) и список людей на фотографии. """

    def get_queryset(self):
        """ Проверяет, есть ли у пользователя доступ к альбому """
        user = self.request.user

        if user.role == UserRoles.ADMIN:
            return Album.objects.all()
        elif user.role == UserRoles.MODERATOR:
            return Album.objects.filter(owner=user)
        return Album.objects.none()

    def post(self, request, pk):
        """ Ищет фото по первичному ключу (pk) только в доступных альбомах.
            - Обновляет поле caption у фото.
            - Возвращает JSON с подтверждением и новой подписью. """
        user = self.request.user
        album = self.get_queryset()

        try:
            photo = Photo.objects.get(pk=pk, album__in=album)
        except Photo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Фото не найдено'}, status=404)

        try:
            data = json.loads(request.body.decode('utf-8'))
            caption = data.get('caption', '').strip()
            people_ids = data.get('people', [])

            photo.caption = caption
            photo.save()

            if isinstance(people_ids, list):
                people_qs = Person.objects.filter(id__in=people_ids)
                photo.people.set(people_qs)
            else:
                photo.people.clear()

            return JsonResponse({'status': 'ok', 'caption': photo.caption})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Некорректный формат JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ошибка обработки данных: {str(e)}'}, status=400)


class PhotoDeleteView(LoginRequiredMixin, View):
    """ Класс удаляет фотографию по её первичному ключу (pk), если пользователь имеет доступ к альбому. """
    def get_queryset(self):
        """ Метод получает список доступных альбомов для текущего пользователя в зависимости от его роли """
        user = self.request.user

        if user.role == UserRoles.ADMIN:
            return Album.objects.all()
        elif user.role == UserRoles.MODERATOR:
            return Album.objects.filter(owner=user)
        return Album.objects.none()

    def post(self, request, pk, *args, **kwargs):
        """ Метод проверяет, принадлежит ли фото одному из этих альбомов. """
        album = self.get_queryset()

        photo = get_object_or_404(Photo, pk=pk, album__in=album)
        photo.delete()
        return JsonResponse({'success': True})

