document.addEventListener('DOMContentLoaded', () => {
  const gallery = document.getElementById('gallery');
  let currentPhotoId = null;

  // Модалки
  const captionModal = document.getElementById('captionModal');
  const deleteModal = document.getElementById('deleteModal');
  const captionInput = document.getElementById('captionInput');
  const cancelBtn = document.getElementById('cancelBtn');
  const saveCaptionBtn = document.getElementById('saveCaptionBtn');
  const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
  const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

  // Открыть модалку редактирования подписи
  gallery.addEventListener('click', e => {
    if (e.target.closest('.edit-btn')) {
      const photoItem = e.target.closest('.isotope-item');
      currentPhotoId = photoItem.dataset.photoId;
      if (!currentPhotoId) return;

      const captionHtml = photoItem.querySelector('a.gallery-single-item').getAttribute('data-sub-html') || '';
      const captionText = captionHtml.replace(/<\/?p>/g, '').trim();

      captionInput.value = captionText;
      openModal(captionModal);
    }

    if (e.target.closest('.delete-btn')) {
      const photoItem = e.target.closest('.isotope-item');
      currentPhotoId = photoItem.dataset.photoId;
      if (!currentPhotoId) return;

      openModal(deleteModal);
    }
  });

  cancelBtn.addEventListener('click', () => {
    closeModal(captionModal);
    currentPhotoId = null;
  });

  cancelDeleteBtn.addEventListener('click', () => {
    closeModal(deleteModal);
    currentPhotoId = null;
  });

  saveCaptionBtn.addEventListener('click', () => {
    if (!currentPhotoId) return;

    const newCaption = captionInput.value.trim();

    fetch(`/gallery/photo/${currentPhotoId}/update_caption/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ caption: newCaption })
    })
    .then(response => {
      if (!response.ok) throw new Error('Ошибка сервера');
      return response.json();
    })
    .then(data => {
      if (data.status === 'ok') {
        const photoItem = document.querySelector(`.isotope-item[data-photo-id="${currentPhotoId}"]`);
        if (photoItem) {
          photoItem.querySelector('a.gallery-single-item').setAttribute('data-sub-html', `<p>${data.caption}</p>`);
        }
        closeModal(captionModal);
        currentPhotoId = null;
      } else {
        alert(data.message || 'Ошибка обновления подписи');
      }
    })
    .catch(err => {
      alert('Ошибка сети или сервера');
      console.error(err);
    });
  });

  confirmDeleteBtn.addEventListener('click', () => {
    if (!currentPhotoId) return;

    fetch(`/gallery/photo/${currentPhotoId}/delete/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
    .then(response => {
      if (!response.ok) throw new Error('Ошибка сервера');
      return response.json();
    })
    .then(data => {
      if (data.success) {
        const photoItem = document.querySelector(`.isotope-item[data-photo-id="${currentPhotoId}"]`);
        if (photoItem) {
          photoItem.remove();
        }
        closeModal(deleteModal);
        currentPhotoId = null;
      } else {
        alert('Ошибка удаления фото');
      }
    })
    .catch(err => {
      alert('Ошибка сети или сервера');
      console.error(err);
    });
  });

  function openModal(modal) {
    modal.style.display = 'flex';
  }

  function closeModal(modal) {
    modal.style.display = 'none';
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
