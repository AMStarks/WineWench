const dialog = document.querySelector('dialog');
const content = dialog.querySelector('.detail');
for (const button of document.querySelectorAll('[data-open]')) {
  button.addEventListener('click', () => {
    const template = document.getElementById(button.dataset.open);
    content.replaceChildren(template.content.cloneNode(true));
    dialog.showModal();
  });
}
dialog.querySelector('.close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  if (event.target === dialog && !event.target.matches(':hover')) dialog.close();
});
