$(document).ready(function() {
  // Отправка формы
  $('#comment-form').on('submit', function(event) {
    event.preventDefault();

    var $form = $(this);
    var url = $form.attr('action');
    var data = $form.serialize();

    $.post(url, data)
      .done(function(response) {
        // Имя
        var authorName = (response.author_first_name || '') + ' ' + (response.author_last_name || '');
        authorName = authorName.trim();

        // Дата
        var createdAt = new Date(response.created_at);
        var options = { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' };
        var formattedDate = createdAt.toLocaleString('ru-RU', options);

        // Аватар
        var avatarHtml = '';
        if (response.author_avatar_url) {
          avatarHtml = '<img src="' + response.author_avatar_url + '" alt="аватар" ' +
               'style="width:30px; height:30px; border-radius:50%; margin-right:8px; vertical-align:middle;">';
        }

        // Если это ответ
        var replyPrefix = '';
        if (response.parent_author_name) {
          replyPrefix = '<span class="reply-to">@' + response.parent_author_name + '</span> ';
        }

        // HTML комментария
            var commentHtml =
              '<div class="' + (response.parent_id ? 'reply' : 'comment') + '" data-id="' + response.id + '">' +
                '<p>' + avatarHtml + '<b>' + authorName + '</b> ' + formattedDate + '</p>' +
                '<p>' + replyPrefix + response.text + '</p>' +
                '<button class="reply-btn" data-comment-id="' + response.id + '">Ответить</button>' +
                (response.parent_id ? '' : '<div class="replies"></div>') +
              '</div>';

            if (response.parent_id) {
              var $parentComment = $('.comment[data-id="' + response.parent_id + '"]');
              var $parentReplies = $parentComment.children('.replies');

              // Если контейнера для ответов нет — создаём
              if ($parentReplies.length === 0) {
                $parentReplies = $('<div class="replies"></div>').appendTo($parentComment);
              }

              $parentReplies.append(commentHtml);
            } else {
              $('#comments').append(commentHtml);
            }

        // Очистка формы
        $form.find('textarea[name="text"]').val('');
        $form.find('input[name="parent_id"]').val('');
        $form.find('textarea[name="text"]').attr('placeholder', 'Ваш комментарий');
      })
      .fail(function(xhr) {
        alert('Ошибка при добавлении комментария: ' + xhr.responseJSON.error);
      });
  });

  // Кнопка «Ответить»
  $('#comments').on('click', '.reply-btn', function() {
    var commentId = $(this).data('comment-id');
    var authorName = $(this).closest('[data-id]').find('b').text().trim();

    $('#comment-form input[name="parent_id"]').val(commentId);
    $('#comment-form textarea[name="text"]').attr('placeholder', 'Ответ @' + authorName);
    $('#comment-form textarea[name="text"]').focus();
  });
});


// Выпадающее меню

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.menu-btn').forEach(button => {
    const menu = button.nextElementSibling;

    button.addEventListener('click', e => {
      e.stopPropagation();

      // Закрыть все открытые меню, кроме текущего
      document.querySelectorAll('.menu-list').forEach(m => {
        if (m !== menu) m.setAttribute('hidden', '');
      });

      // Переключить видимость текущего меню
      if (menu.hasAttribute('hidden')) {
        menu.removeAttribute('hidden');
        button.setAttribute('aria-expanded', 'true');
      } else {
        menu.setAttribute('hidden', '');
        button.setAttribute('aria-expanded', 'false');
      }
    });
  });

  // Закрыть меню, если клик вне кнопок меню и меню
  document.addEventListener('click', () => {
    document.querySelectorAll('.menu-list').forEach(menu => {
      menu.setAttribute('hidden', '');
      const btn = menu.previousElementSibling;
      if (btn && btn.classList.contains('menu-btn')) {
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  });
});


// Удаление

// Делегирование для меню
$('#comments').on('click', '.menu-btn', function(e) {
  e.stopPropagation();
  const menu = $(this).next('.menu-list');
  $('.menu-list').not(menu).attr('hidden', true);
  const isHidden = menu.attr('hidden') !== undefined;
  if (isHidden) {
    menu.removeAttr('hidden');
    $(this).attr('aria-expanded', 'true');
  } else {
    menu.attr('hidden', true);
    $(this).attr('aria-expanded', 'false');
  }
});

// Закрыть меню при клике вне
$(document).on('click', function() {
  $('.menu-list').attr('hidden', true);
  $('.menu-btn').attr('aria-expanded', 'false');
});

// Делегирование для удаления
$('#comments').on('click', '.delete-comment-btn', function(e) {
  e.preventDefault();
  if (!confirm('Удалить комментарий?')) return;

  const url = $(this).data('url');
  // Ищем ближайший контейнер комментария или ответа
  const $commentDiv = $(this).closest('.comment, .reply');

  fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Accept': 'application/json',
    },
  })
  .then(response => response.ok ? response.json() : Promise.reject())
  .then(data => {
    if (data.success) {
      $commentDiv.remove();
    } else {
      alert('Ошибка при удалении');
    }
  })
  .catch(() => alert('Ошибка при запросе'));
});

