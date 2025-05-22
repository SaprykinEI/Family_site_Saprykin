function showInfo(card) {
  const info = card.querySelector('.person-info');
  if (info) {
    info.classList.add('visible');
  }
}

function hideInfo(card) {
  const info = card.querySelector('.person-info');
  if (info) {
    info.classList.remove('visible');
  }
}
