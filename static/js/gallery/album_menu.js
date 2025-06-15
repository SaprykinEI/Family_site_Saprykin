
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.options-button').forEach(button => {
        button.addEventListener('click', function (e) {
            e.stopPropagation();
            const menu = this.nextElementSibling;
            menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
        });
    });

    // Закрытие меню при клике вне его
    document.addEventListener('click', function () {
        document.querySelectorAll('.options-menu').forEach(menu => {
            menu.style.display = 'none';
        });
    });
});

