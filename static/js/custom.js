$(document).ready(function() {
  $('.project-carousel').owlCarousel({
    items: 4,
    margin: 0,
    dots: false,
    nav: true,
    responsive: {
      0: { items: 1 },
      768: { items: 2 },
      992: { items: 3 },
      1200: { items: 4 }
    }
  });

  $('.project-carousel').lightGallery({
    selector: 'a.cc-item',
    download: false,
    counter: false,
    closable: true,
  });
});


document.addEventListener('DOMContentLoaded', () => {
  const dropdown = document.getElementById('userDropdown');
  if (!dropdown) return;

  const menu = dropdown.querySelector('.dropdown-menu');
  let hideTimeout = null;

  dropdown.addEventListener('mouseenter', () => {
    clearTimeout(hideTimeout);
    menu.style.display = 'block';
  });

  dropdown.addEventListener('mouseleave', () => {
    hideTimeout = setTimeout(() => {
      menu.style.display = 'none';
    }, 300); // Задержка скрытия меню
  });
});
