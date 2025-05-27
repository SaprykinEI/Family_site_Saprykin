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
