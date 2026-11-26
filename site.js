const form = document.querySelector('.filters');
if (form) {
  const cards = [...document.querySelectorAll('.card')];
  const query = form.elements.q;
  const category = form.elements.category;
  const status = document.querySelector('.count');
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  function filter() {
    let shown = 0;
    for (const card of cards) {
      const matches = normalize(card.textContent).includes(normalize(query.value)) &&
        (!category.value || card.dataset.categories.split('|').includes(category.value));
      card.hidden = !matches;
      if (matches) shown++;
    }
    status.textContent = shown ? shown + (shown === 1 ? ' story' : ' stories') : 'No stories found. Try another search or category.';
    const url = new URL(location.href);
    for (const field of [query, category]) {
      if (field.value) url.searchParams.set(field.name, field.value);
      else url.searchParams.delete(field.name);
    }
    history.replaceState(null, '', url);
  }
  const params = new URLSearchParams(location.search);
  query.value = params.get('q') || '';
  category.value = params.get('category') || '';
  form.addEventListener('input', filter);
  form.addEventListener('submit', event => { event.preventDefault(); filter(); });
  form.addEventListener('reset', () => requestAnimationFrame(filter));
  filter();
}
