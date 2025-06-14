Dropzone.options.mediaDropzone = {
  paramName: 'file',
  maxFilesize: 100, // MB
  acceptedFiles: 'image/*,video/*',
  addRemoveLinks: true,
  dictDefaultMessage: 'Перетащите файлы сюда или нажмите для выбора',
  success: function (file, response) {
    console.log('Загружено:', response);
  },
  error: function (file, response) {
    console.error('Ошибка загрузки:', response);
  }
};
