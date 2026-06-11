document.addEventListener('DOMContentLoaded', function () {
  const imgs = Array.from(document.querySelectorAll('.grid img'));
  if (!imgs.length) return;

  // Create lightbox elements
  const lb = document.createElement('div');
  lb.id = 'lightbox';
  lb.innerHTML = `
    <div class="container">
      <button class="nav-btn prev" aria-label="Previous">◀</button>
      <img src="" alt="" />
      <button class="nav-btn next" aria-label="Next">▶</button>
      <button class="close" aria-label="Close">✕</button>
      <div class="caption" aria-hidden="true"></div>
    </div>`;
  document.body.appendChild(lb);

  const lbImg = lb.querySelector('img');
  const caption = lb.querySelector('.caption');
  const btnPrev = lb.querySelector('.prev');
  const btnNext = lb.querySelector('.next');
  const btnClose = lb.querySelector('.close');

  let current = 0;

  // Store original filename in data attribute and remove visible filenames
  imgs.forEach((el) => {
    const original = el.getAttribute('alt') || (el.getAttribute('src') || '').split('/').pop() || '';
    el.dataset.filename = original;
    el.removeAttribute('title');
    // Remove alt attribute so filenames are not exposed
    el.removeAttribute('alt');
    // Disable right-click on each image
    el.addEventListener('contextmenu', (e) => e.preventDefault());
  });

  function showAt(index) {
    current = (index + imgs.length) % imgs.length;
    const src = imgs[current].getAttribute('src');
    lbImg.src = src;
    lbImg.removeAttribute('alt');
    caption.textContent = `Image ${current + 1} of ${imgs.length}`;
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function hide() {
    lb.classList.remove('open');
    lbImg.src = '';
    document.body.style.overflow = '';
  }

  imgs.forEach((el, i) => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      showAt(i);
    });
  });

  btnPrev.addEventListener('click', () => showAt(current - 1));
  btnNext.addEventListener('click', () => showAt(current + 1));
  btnClose.addEventListener('click', hide);

  lb.addEventListener('click', (e) => {
    if (e.target === lb) hide();
  });

  // Prevent right-click inside the lightbox
  lb.addEventListener('contextmenu', (e) => e.preventDefault());

  // Touch swipe support for mobile: detect horizontal swipes on the lightbox container
  let touchStartX = 0;
  const touchThreshold = 50; // pixels
  const container = lb.querySelector('.container');
  container.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].clientX;
  }, {passive: true});
  container.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > touchThreshold) {
      if (dx < 0) showAt(current + 1);
      else showAt(current - 1);
    }
  });

  document.addEventListener('keydown', (e) => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'ArrowLeft') showAt(current - 1);
    if (e.key === 'ArrowRight') showAt(current + 1);
    if (e.key === 'Escape') hide();
  });
});
