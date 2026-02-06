const header = document.getElementById('header');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileNav = document.getElementById('mobileNav');

// Header efeito scroll
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 30);
});

// Menu mobile
mobileMenuBtn.addEventListener('click', () => {
  mobileNav.classList.toggle('active');
});
