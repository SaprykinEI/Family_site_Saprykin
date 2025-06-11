from django.views.generic import ListView
from django.db.models import Q, F, Value, CharField
from django.db.models.functions import ExtractYear
from gallery.models import Album, Category, Tag
from family_tree.models import Person


class AlbumListView(ListView):
    model = Album
    template_name = 'gallery/albums_list.html'  # адаптируй под свой шаблон
    context_object_name = 'albums'
    paginate_by = 12  # если нужна пагинация

    def get_queryset(self):
        qs = Album.objects.all().select_related('category').prefetch_related(
            'photos__tags', 'photos__people', 'videos__tags', 'videos__people'
        ).distinct()

        category_ids = self.request.GET.getlist('category')
        years = self.request.GET.getlist('year')
        tag_ids = self.request.GET.getlist('tag')
        person_id = self.request.GET.get('person')  # одно значение
        search = self.request.GET.get('search', '').strip()

        if category_ids:
            qs = qs.filter(category__id__in=category_ids)

        if years:
            years_int = [int(y) for y in years if y.isdigit()]
            if years_int:
                qs = qs.annotate(year=ExtractYear('date')).filter(year__in=years_int)

        if tag_ids:
            qs = qs.filter(
                Q(photos__tags__id__in=tag_ids) | Q(videos__tags__id__in=tag_ids)
            )

        if person_id and person_id.isdigit():
            qs = qs.filter(
                Q(photos__people__id=person_id) | Q(videos__people__id=person_id)
            )

        if search:
            qs = qs.filter(title__icontains=search)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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

        return context