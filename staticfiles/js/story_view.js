document.addEventListener("DOMContentLoaded", () => {
  const progress = document.querySelector(".progress");
  setTimeout(() => {
    window.history.back(); // Auto close after 5s
  }, 5000);
});
