new Swiper('.card-wrapper', {
    spaceBetween: 30,
    loop: true,
  
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
      dynamicBullets: true,
    },
  
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
     
    //Responsibidad
    breakpoints: {
      0 : {
        slidesPerView: 1
      },
      768 : {
        slidesPerView: 2
      },
      1024 : {
        slidesPerView: 3
      },
    }
  });