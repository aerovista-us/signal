
(() => {
  const $ = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => [...r.querySelectorAll(s)];

  const progress = $('.progress-line');
  const updateProgress = () => {
    if (!progress) return;
    const d = document.documentElement;
    const max = d.scrollHeight - d.clientHeight;
    progress.style.width = `${max ? (d.scrollTop / max) * 100 : 0}%`;
  };
  document.addEventListener('scroll', updateProgress, {passive:true});
  updateProgress();

  const menu = $('.mobile-menu');
  const nav = $('.main-nav');
  if (menu && nav) menu.addEventListener('click', () => nav.classList.toggle('open'));

  $$('.print-button').forEach(b => b.addEventListener('click', () => window.print()));

  const imageModal = $('#image-modal');
  const modalImage = imageModal ? $('img', imageModal) : null;
  $$('.image-button').forEach(btn => btn.addEventListener('click', () => {
    if (!imageModal || !modalImage) return;
    modalImage.src = btn.dataset.image;
    imageModal.classList.add('open');
  }));
  if (imageModal) {
    $('.modal-close', imageModal)?.addEventListener('click', () => imageModal.classList.remove('open'));
    imageModal.addEventListener('click', e => { if (e.target === imageModal) imageModal.classList.remove('open'); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') imageModal.classList.remove('open'); });
  }

  // Homepage episode player
  const episodeButtons = $$('.episode-button');
  const mainAudio = $('#main-audio');
  const playerTitle = $('#player-title');
  const playerSubtitle = $('#player-subtitle');
  const playerTranscript = $('#player-transcript');
  const playerReport = $('#player-report-link');
  const playerTranscriptLink = $('#player-transcript-link');
  const audioStatus = $('#main-audio-status');

  const selectEpisode = btn => {
    episodeButtons.forEach(b => b.classList.toggle('active', b === btn));
    if (playerTitle) playerTitle.textContent = btn.dataset.title;
    if (playerSubtitle) playerSubtitle.textContent = btn.dataset.subtitle;
    if (playerTranscript) playerTranscript.textContent = btn.dataset.preview;
    if (playerReport) playerReport.href = btn.dataset.report;
    if (playerTranscriptLink) playerTranscriptLink.href = btn.dataset.transcript;
    if (mainAudio) {
      mainAudio.src = btn.dataset.audio;
      mainAudio.load();
      if (audioStatus) audioStatus.textContent = `Looking for ${btn.dataset.audio.split('/').pop()}…`;
    }
  };
  episodeButtons.forEach(btn => btn.addEventListener('click', () => selectEpisode(btn)));
  if (episodeButtons[0]) selectEpisode(episodeButtons[0]);

  const audioErrorHandler = (audio, status) => {
    if (!audio || !status) return;
    audio.addEventListener('canplay', () => status.textContent = 'Audio file found and ready.');
    audio.addEventListener('error', () => status.textContent = 'MP3 not included yet. The complete transcript is available now; add the named MP3 to /audio when rendered.');
  };
  audioErrorHandler(mainAudio, audioStatus);
  $$('.detail-audio').forEach(audio => audioErrorHandler(audio, audio.parentElement.querySelector('.audio-status')));

  // Division filter
  const chips = $$('.filter-chip');
  const divCards = $$('.division-card');
  chips.forEach(chip => chip.addEventListener('click', () => {
    chips.forEach(c => c.classList.toggle('active', c === chip));
    const filter = chip.dataset.filter;
    divCards.forEach(card => {
      card.hidden = filter !== 'all' && !card.dataset.category.toLowerCase().includes(filter.toLowerCase());
    });
  }));

  // Search source library and visible cards
  const search = $('#report-search');
  if (search) {
    search.addEventListener('input', () => {
      const q = search.value.trim().toLowerCase();
      $$('[data-searchable]').forEach(el => {
        el.hidden = q && !el.textContent.toLowerCase().includes(q);
      });
    });
  }

  // Page review status
  $$('.review-toggle input').forEach(box => {
    const key = `av-report-reviewed:${box.dataset.page}`;
    box.checked = localStorage.getItem(key) === '1';
    box.addEventListener('change', () => localStorage.setItem(key, box.checked ? '1' : '0'));
  });

  // Copy deep link
  $$('.copy-link').forEach(btn => btn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(location.href);
      const old = btn.textContent;
      btn.textContent = 'Link copied';
      setTimeout(() => btn.textContent = old, 1300);
    } catch (_) {}
  }));
})();
