// Add this at the top of main.js
// main.js
window.addEventListener("load", function () {
  const loader = document.querySelector(".loader");
  setTimeout(function () {
    loader.classList.add("loader-hidden");
    loader.addEventListener("transitionend", function () {
      document.body.removeChild(loader);
    });
  }, 1000);
});

// Main JavaScript for interactive elements
document.addEventListener("DOMContentLoaded", function () {
  const mobileMenuToggle = document.createElement("div");
  mobileMenuToggle.className = "mobile-menu-toggle";
  mobileMenuToggle.innerHTML = '<i class="fas fa-bars"></i>';

  const mobileMenu = document.createElement("div");
  mobileMenu.className = "mobile-menu";

  // Clone desktop nav items for mobile menu
  const navClone = document.querySelector("nav ul").cloneNode(true);
  const authClone = document.querySelector(".auth-buttons").cloneNode(true);

  mobileMenu.appendChild(navClone);
  mobileMenu.appendChild(authClone);

  const menuOverlay = document.createElement("div");
  menuOverlay.className = "menu-overlay";

  document.body.appendChild(mobileMenu);
  document.body.appendChild(menuOverlay);

  // Insert toggle button in header
  document.querySelector("header").appendChild(mobileMenuToggle);

  // Update the mobile menu toggle event listener
  mobileMenuToggle.addEventListener("click", function () {
    document.body.classList.toggle("mobile-menu-open");
    mobileMenu.classList.toggle("active");
    menuOverlay.classList.toggle("active");
    mobileMenuToggle.innerHTML = mobileMenu.classList.contains("active")
      ? '<i class="fas fa-times"></i>'
      : '<i class="fas fa-bars"></i>';
  });

  // Close menu when clicking overlay
  menuOverlay.addEventListener("click", function () {
    mobileMenu.classList.remove("active");
    menuOverlay.classList.remove("active");
    mobileMenuToggle.innerHTML = '<i class="fas fa-bars"></i>';
    document.body.classList.remove("mobile-menu-open");
  });
  // Close menu when clicking a link
  mobileMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", function () {
      mobileMenu.classList.remove("active");
      menuOverlay.classList.remove("active");
      mobileMenuToggle.innerHTML = '<i class="fas fa-bars"></i>';
    });
  }); // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute("href")).scrollIntoView({
        behavior: "smooth",
      });
    });
  });

  // Animate stats cards on scroll
  const statsObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animated");
        }
      });
    },
    { threshold: 0.1 }
  );

  document.querySelectorAll(".stat-card").forEach((card) => {
    statsObserver.observe(card);
  });

  // Toggle Earth rotation on click
  document
    .getElementById("earth-container")
    .addEventListener("click", function () {
      isRotating = !isRotating;
    });

  // Mobile menu toggle (would be added if implementing mobile menu)
  // const mobileMenuToggle = document.createElement('div');
  // mobileMenuToggle.className = 'mobile-menu-toggle';
  // ...
});
