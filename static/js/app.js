document.addEventListener("submit", (e) => {
  if (e.target.classList.contains("js-confirm-delete")) {
    if (!confirm("Delete this booking?")) e.preventDefault();
  }
});
