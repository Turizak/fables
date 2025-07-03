// Hamburger menu functionality
document.addEventListener('DOMContentLoaded', function() {
  const navToggle = document.querySelector('.nav-toggle');
  const navMenu = document.querySelector('.nav-menu');
  
  // Toggle mobile menu
  navToggle.addEventListener('click', function() {
    const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
    
    navToggle.setAttribute('aria-expanded', !isExpanded);
    navToggle.classList.toggle('active');
    navMenu.classList.toggle('active');
  });
  
  // Close menu when clicking outside
  document.addEventListener('click', function(event) {
    const isClickInsideNav = navToggle.contains(event.target) || navMenu.contains(event.target);
    
    if (!isClickInsideNav && navMenu.classList.contains('active')) {
      navToggle.setAttribute('aria-expanded', 'false');
      navToggle.classList.remove('active');
      navMenu.classList.remove('active');
    }
  });
  
  // Close menu when clicking on nav links (mobile)
  const navLinks = document.querySelectorAll('.nav-links a');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      if (window.innerWidth <= 768) {
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.classList.remove('active');
        navMenu.classList.remove('active');
      }
    });
  });
});