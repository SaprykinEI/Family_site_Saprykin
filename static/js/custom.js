// Проверка кликов по ссылкам — временный код
document.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', function(e) {
        // Убедись, что здесь нет event.preventDefault()
        // console.log('Clicked:', a.href);
    });
});
