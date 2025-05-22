document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.price').forEach(el => {
    const price = Number(el.getAttribute('data-price'));
    const showEach = el.getAttribute('data-each') === 'true';

    if (!isNaN(price)) {
      el.textContent = 'Rp ' + price.toLocaleString('id-ID');
      if (showEach) {
        el.textContent += ' each';
      }
    }
  });
});
