document.addEventListener("DOMContentLoaded", function () {
  // Create glitter container
  const glitter = document.createElement("div");
  glitter.className = "glitter";
  document.body.appendChild(glitter);

  // Create particles for the whole page - fewer, slower particles
  createGlitterParticles(glitter, 210, {
    minSize: 1,
    maxSize: 3,
    animationDuration: [60, 100], // Much slower movement
    fallDistance: "200vh", // Longer falling distance
    opacityRange: [0.2, 0.8], // More subtle appearance
  });

  // Add enhanced deep space glitter to dark sections with more particles
  document
    .querySelectorAll(
      ".mission-section, .data-section , data-hero,data-explorer, data-sources ,auth-container ,.hero-sectiondata "
    )
    .forEach((section) => {
      const sectionGlitter = document.createElement("div");
      sectionGlitter.className = "glitter dark-section";
      section.appendChild(sectionGlitter);
      createGlitterParticles(sectionGlitter, 150, {
        // Increased from 25 to 60 particles
        color: "rgba(156, 216, 228, 0.88)",
        animationDuration: [80, 160],
        fallDistance: "150vh",
        minSize: 1,
        maxSize: 3, // Increased max size from 2 to 3
        opacityRange: [0.2, 0.7], // Increased opacity range
        animationType: Math.random() > 0.7 ? "twinkle" : "fall", // 30% chance of twinkling
      });
    });

  function createGlitterParticles(container, count, options = {}) {
    const {
      minSize = 1,
      maxSize = 3,
      color = "rgba(255, 255, 255, 0.8)",
      animationDuration = [30, 60],
      animationType = "fall",
      fallDistance = "100vh",
      opacityRange = [0.3, 0.9],
    } = options;

    for (let i = 0; i < count; i++) {
      const particle = document.createElement("div");
      particle.className = "glitter-particle";

      // Randomize properties
      const size = Math.random() * (maxSize - minSize) + minSize;
      const duration =
        Math.random() * (animationDuration[1] - animationDuration[0]) +
        animationDuration[0];
      const delay = Math.random() * -duration;
      const left = Math.random() * 100;
      const top = animationType === "twinkle" ? Math.random() * 100 : -10;
      const opacity =
        Math.random() * (opacityRange[1] - opacityRange[0]) + opacityRange[0];

      // Apply base styles
      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;
      particle.style.left = `${left}%`;
      particle.style.top = `${top}%`;
      particle.style.opacity = opacity;
      particle.style.background = color;
      particle.style.willChange = "transform, opacity";

      // Set animation based on type
      if (animationType === "twinkle") {
        // Twinkling stars that pulse in place
        particle.style.position = "absolute";
        particle.style.animation = `twinkle ${duration}s ease-in-out ${delay}s infinite alternate`;
        particle.style.borderRadius = "50%";
        particle.style.boxShadow = `0 0 ${size * 2}px ${
          size / 2
        }px rgba(255, 255, 255, 0.3)`;
      } else {
        // Slow falling particles
        particle.style.animation = `glitter-fall ${duration}s linear ${delay}s infinite`;
        particle.style.setProperty("--fall-distance", fallDistance);

        // Random shape variation
        if (Math.random() > 0.8) {
          particle.style.borderRadius = "0";
          particle.style.transform = `rotate(${Math.random() * 360}deg)`;
        } else {
          particle.style.borderRadius = "50%";
        }
      }

      container.appendChild(particle);
    }
  }
});
