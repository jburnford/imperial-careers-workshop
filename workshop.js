(() => {
  function prepareTables(root = document) {
    root.querySelectorAll('table:not(.workshop-table)').forEach(table => {
      const header = table.tHead?.rows[0] || table.rows[0];
      if (!header || !header.querySelector('th')) return;
      const labels = [...header.cells].map(cell => cell.textContent.trim());
      table.classList.add('workshop-table');
      table.setAttribute('role', 'table');
      header.classList.add('workshop-table-head');
      [...table.rows].forEach(row => {
        row.setAttribute('role', 'row');
        [...row.cells].forEach((cell, i) => {
          cell.setAttribute('role', cell.tagName === 'TH' ? 'columnheader' : 'cell');
          if (row !== header && labels[i]) cell.dataset.label = labels[i];
        });
      });
    });
  }

  function setupReadingView() {
    const reveal = window.Reveal;
    if (!reveal?.isReady()) return;
    // Touch screens only: a 1024-pixel projector or a scaled laptop must stay in presentation mode.
    // ?present forces the slide view on any device.
    const media = matchMedia('(max-width: 1024px) and (pointer: coarse)');
    const forcePresent = new URLSearchParams(location.search).has('present');
    // Reveal's default phone view scales a full slide down; use readable text instead.
    reveal.configure({scrollActivationWidth: 0});
    const nav = document.createElement('nav');
    nav.className = 'workshop-reading-nav';
    nav.setAttribute('aria-label', 'Slide reading view');
    nav.innerHTML = '<a href="index.html">Workshop home</a><span>Slides · scroll to read</span>';
    document.body.prepend(nav);
    const exposeSlides = () => {
      if (!document.documentElement.classList.contains('workshop-reading')) return;
      reveal.getSlides().forEach(slide => {
        slide.removeAttribute('hidden');
        slide.removeAttribute('aria-hidden');
      });
    };
    const update = () => {
      const reading = media.matches && !forcePresent && !reveal.isPrintView() && !reveal.isSpeakerNotes();
      document.documentElement.classList.toggle('workshop-reading', reading);
      reveal.configure({keyboard: !reading, touch: !reading, autoPlayMedia: reading ? false : null});
      if (reading) {
        exposeSlides();
        // Reveal only loads nearby slides. Native lazy loading covers the full document.
        reveal.getRevealElement().querySelectorAll('img[data-src]').forEach(image => {
          image.loading = 'lazy';
          image.src = image.dataset.src;
          image.removeAttribute('data-src');
        });
        reveal.getRevealElement().querySelectorAll('video').forEach(video => video.pause());
      } else {
        reveal.sync();
      }
    };
    media.addEventListener('change', update);
    reveal.on('slidechanged', exposeSlides);
    update();
  }

  function init() {
    prepareTables();
    // Exercise comparisons insert their tables only after participants click Compare.
    document.querySelectorAll('#mine, #theirs').forEach(root => {
      new MutationObserver(() => prepareTables(root)).observe(root, {childList: true});
    });
    if (document.querySelector('.reveal')) {
      if (window.Reveal?.isReady()) setupReadingView();
      else window.Reveal?.on('ready', setupReadingView);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
