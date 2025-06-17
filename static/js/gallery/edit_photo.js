document.addEventListener('DOMContentLoaded', () => {
  console.log('edit_photo.js загружен');

  const captionModal = document.getElementById('captionModal');
  const cancelBtn = document.getElementById('cancelBtn');

  const editButtons = document.querySelectorAll('.edit-caption-btn');
  console.log('Найдено кнопок редактирования:', editButtons.length);

  editButtons.forEach(button => {
    button.addEventListener('click', () => {
      console.log('Нажата кнопка редактирования');
      captionModal.style.display = 'flex'; // показываем модалку
    });
  });

  cancelBtn.addEventListener('click', () => {
    captionModal.style.display = 'none';
  });

  window.addEventListener('click', e => {
    if (e.target === captionModal) {
      captionModal.style.display = 'none';
    }
  });
});
