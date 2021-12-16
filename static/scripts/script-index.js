
  // Variable que controlar cual imagen se despliega
  var slideIndex = 1;
    
  // Función que muestra la imagen actual
  showSlides(slideIndex);

  // Función que muestra el slide de acuerdo al numero indicado
  function plusSlides(n) 
  {
      showSlides(slideIndex += n);
  }

  // Función que actualiza la imagen
  function currentSlide(n) 
  {
      showSlides(slideIndex = n);
  }

  // Función que muestra la imagen
  function showSlides(n) 
  {
      var i;
      var slides = document.getElementsByClassName("mySlides");
      var dots = document.getElementsByClassName("dot");
      if (n > slides.length) {slideIndex = 1}    
      if (n < 1) {slideIndex = slides.length}
      for (i = 0; i < slides.length; i++) 
      {
          slides[i].style.display = "none";  
      }
      for (i = 0; i < dots.length; i++) 
      {
          dots[i].className = dots[i].className.replace(" active", "");
      }
      slides[slideIndex-1].style.display = "block";  
      dots[slideIndex-1].className += " active";
  }          
