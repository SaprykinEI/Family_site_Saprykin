document.addEventListener('DOMContentLoaded', () => {
  const favoriteBtn = document.querySelector('.favorite-btn');
  if (!favoriteBtn) return;

  favoriteBtn.addEventListener('click', () => {
    const albumSlug = favoriteBtn.dataset.albumSlug;
    const csrftoken = getCookie('csrftoken');

    fetch(`/gallery/album/${albumSlug}/toggle-like/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({})  // тело можно оставить пустым, если не нужно
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }

      // Обновляем иконки
      const heartEmpty = favoriteBtn.querySelector('.icon-heart-empty');
      const heartFilled = favoriteBtn.querySelector('.icon-heart-filled');
      if (data.liked) {
        heartEmpty.classList.remove('visible');
        heartFilled.classList.add('visible');
      } else {
        heartEmpty.classList.add('visible');
        heartFilled.classList.remove('visible');
      }

      // Обновляем количество лайков
      favoriteBtn.querySelector('.fav-count').textContent = data.like_count;
    })
    .catch(error => {
      console.error('Ошибка:', error);
      alert('Произошла ошибка при лайке. Попробуйте позже.');
    });
  });
});

// Функция для получения CSRF токена из куки (Django по умолчанию)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Проверяем, начинается ли кука с нужного имени
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
