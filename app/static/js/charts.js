// Initialize data charts
document.addEventListener("DOMContentLoaded", function () {
  // Temperature Chart
  const tempCtx = document.getElementById("temp-graph").getContext("2d");
  new Chart(tempCtx, {
    type: "line",
    data: {
      labels: ["1880", "1900", "1920", "1940", "1960", "1980", "2000", "2020"],
      datasets: [
        {
          label: "Global Temperature Anomaly (°C)",
          data: [-0.2, -0.1, -0.05, 0.1, 0.2, 0.4, 0.8, 1.2],
          borderColor: "#ff6b6b",
          backgroundColor: "rgba(255, 107, 107, 0.1)",
          borderWidth: 3,
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
      },
      scales: {
        y: {
          grid: { color: "rgba(255, 255, 255, 0.1)" },
          ticks: { color: "rgba(255, 255, 255, 0.7)" },
        },
        x: {
          grid: { color: "rgba(255, 255, 255, 0.1)" },
          ticks: { color: "rgba(255, 255, 255, 0.7)" },
        },
      },
    },
  });

  // CO2 Chart
  const co2Ctx = document.getElementById("co2-graph").getContext("2d");
  new Chart(co2Ctx, {
    type: "line",
    data: {
      labels: ["1960", "1970", "1980", "1990", "2000", "2010", "2020"],
      datasets: [
        {
          label: "Atmospheric CO₂ (ppm)",
          data: [320, 330, 340, 355, 370, 390, 419],
          borderColor: "#4ecdc4",
          backgroundColor: "rgba(78, 205, 196, 0.1)",
          borderWidth: 3,
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
      },
      scales: {
        y: {
          grid: { color: "rgba(255, 255, 255, 0.1)" },
          ticks: { color: "rgba(255, 255, 255, 0.7)" },
        },
        x: {
          grid: { color: "rgba(255, 255, 255, 0.1)" },
          ticks: { color: "rgba(255, 255, 255, 0.7)" },
        },
      },
    },
  });
});
