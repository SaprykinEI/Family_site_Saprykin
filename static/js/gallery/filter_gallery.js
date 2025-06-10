// static/js/gallery/filter_gallery.js
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем наличие jQuery
    if (typeof jQuery === 'undefined') {
        console.error('jQuery is not loaded. Please include jQuery before this script.');
        return;
    }

    // Проверяем наличие Isotope
    if (typeof $.fn.isotope === 'undefined') {
        console.error('Isotope is not loaded. Please include Isotope before this script.');
        return;
    }

    // Проверяем наличие imagesLoaded (если используется)
    if (typeof $.fn.imagesLoaded === 'undefined') {
        console.warn('imagesLoaded is not loaded. Layout may not work properly.');
    }

    try {
        // Инициализация Isotope
        var $grid = $('.isotope-items-wrap').isotope({
            itemSelector: '.isotope-item',
            layoutMode: 'fitRows',
            percentPosition: true,
            masonry: {
                columnWidth: '.grid-sizer'
            }
        });

        // Фильтрация по категориям
        $('.isotope-filter-links').on('click', 'a', function(e) {
            e.preventDefault();
            var filterValue = $(this).attr('data-filter');
            
            try {
                $grid.isotope({ filter: filterValue });
                $('.isotope-filter-links a').removeClass('active');
                $(this).addClass('active');
            } catch (error) {
                console.error('Isotope filter error:', error);
            }
        });

        // Фильтрация по году
        $('#year-filter').on('change', function() {
            var year = $(this).val();
            var filter = year === '*' ? '*' : '.year-' + year;
            
            try {
                $grid.isotope({ filter: filter });
                
                // Обновляем URL без перезагрузки страницы
                var url = new URL(window.location.href);
                if (year === '*') {
                    url.searchParams.delete('year');
                } else {
                    url.searchParams.set('year', year);
                }
                window.history.pushState({}, '', url);
            } catch (error) {
                console.error('Year filter error:', error);
            }
        });

        // Фильтрация по тегам и людям (через URL)
        $('.tag-cloud').on('click', 'a', function(e) {
            e.preventDefault();
            window.location.href = $(this).attr('href');
        });

        // Поиск по названию с задержкой
        var searchTimeout;
        $('#album-search').on('keyup', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                var searchText = $('#album-search').val().toLowerCase();
                
                try {
                    $grid.isotope({
                        filter: function() {
                            var title = $(this).find('.gl-item-title').text().toLowerCase();
                            return title.includes(searchText);
                        }
                    });
                } catch (error) {
                    console.error('Search error:', error);
                }
            }, 300); // 300ms задержка
        });

        // Инициализация после загрузки изображений (если imagesLoaded доступен)
        if (typeof $.fn.imagesLoaded !== 'undefined') {
            $grid.imagesLoaded().progress(function() {
                $grid.isotope('layout');
            });
        }

        // Применяем фильтры из URL при загрузке страницы
        function applyUrlFilters() {
            try {
                const urlParams = new URLSearchParams(window.location.search);
                const year = urlParams.get('year');
                const category = urlParams.get('category');

                if (year) {
                    $('#year-filter').val(year).trigger('change');
                }
                
                if (category) {
                    $('.isotope-filter-links a[data-filter=".category-' + category + '"]').click();
                }
            } catch (error) {
                console.error('URL filter application error:', error);
            }
        }

        applyUrlFilters();

        // Обработка кнопки "Назад" в браузере
        window.addEventListener('popstate', function() {
            applyUrlFilters();
        });

    } catch (error) {
        console.error('Gallery initialization error:', error);
    }
});