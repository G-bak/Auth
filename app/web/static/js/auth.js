(function () {
  const form = document.querySelector('form');
  if (!form) return;
  form.addEventListener('submit', function () {
    form.classList.add('is-loading');
  });
})();