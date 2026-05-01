/* ── Mobile Menu ── */
const hamburger = document.querySelector('.hamburger');
const mobileNav = document.querySelector('.mobile-nav');
if (hamburger && mobileNav) {
  hamburger.addEventListener('click', () => {
    mobileNav.classList.toggle('open');
  });
}

/* ── FAQ Accordion ── */
document.querySelectorAll('.faq-question').forEach(q => {
  q.addEventListener('click', () => {
    const item = q.closest('.faq-item');
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});

/* ── Blog Filter ── */
const filterBtns = document.querySelectorAll('.filter-btn');
const articleCards = document.querySelectorAll('.article-card[data-cat]');
filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.dataset.cat;
    articleCards.forEach(card => {
      card.style.display = (cat === 'todos' || card.dataset.cat === cat) ? '' : 'none';
    });
  });
});

/* ── Reading Time ── */
const postBody = document.querySelector('.post-body');
const readingTimeEl = document.querySelector('.reading-time');
if (postBody && readingTimeEl) {
  const words = postBody.innerText.trim().split(/\s+/).length;
  const mins = Math.max(1, Math.round(words / 200));
  readingTimeEl.textContent = `${mins} min de leitura`;
}

/* ── Contact Form ── */
const contactForm = document.querySelector('#contact-form');
if (contactForm) {
  contactForm.addEventListener('submit', e => {
    e.preventDefault();
    const nome = contactForm.querySelector('[name="nome"]').value.trim();
    const telefone = contactForm.querySelector('[name="telefone"]').value.trim();
    if (!nome || !telefone) {
      alert('Por favor, preencha nome e telefone.');
      return;
    }
    if (typeof gtag === 'function') {
      gtag('event', 'close_convert_lead');
    }
    const successEl = document.querySelector('.form-success');
    if (successEl) {
      contactForm.style.display = 'none';
      successEl.classList.add('visible');
    }
  });
}

/* ── WhatsApp Click Tracking ── */
document.addEventListener('click', e => {
  const link = e.target.closest('a[href*="wa.me"]');
  if (link && typeof gtag === 'function') {
    gtag('event', 'CliqueWhatsapp');
  }
});

/* ── Admin: Slug auto-generation ── */
const titleInput = document.querySelector('#post-title');
const slugInput = document.querySelector('#post-slug');
if (titleInput && slugInput) {
  titleInput.addEventListener('input', () => {
    const slug = titleInput.value
      .toLowerCase()
      .normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/[^a-z0-9\s-]/g, '')
      .trim()
      .replace(/\s+/g, '-');
    slugInput.value = slug;
    updateGooglePreview();
  });
}

/* ── Admin: Char counters ── */
function setupCounter(inputId, counterId, maxChars, progressId) {
  const input = document.querySelector(inputId);
  const counter = document.querySelector(counterId);
  const progress = document.querySelector(progressId);
  if (!input) return;
  const update = () => {
    const len = input.value.length;
    if (counter) counter.textContent = `${len}/${maxChars}`;
    if (progress) {
      const pct = Math.min(100, (len / maxChars) * 100);
      progress.style.width = pct + '%';
      progress.style.background = len > maxChars ? '#ef5350' : len >= maxChars * 0.8 ? '#ffc107' : 'var(--primary)';
    }
    updateGooglePreview();
  };
  input.addEventListener('input', update);
  update();
}
setupCounter('#meta-title', '#meta-title-count', 60, '#meta-title-progress');
setupCounter('#meta-desc', '#meta-desc-count', 160, '#meta-desc-progress');

/* ── Admin: Google Preview ── */
function updateGooglePreview() {
  const titleEl = document.querySelector('#meta-title');
  const descEl = document.querySelector('#meta-desc');
  const slugEl = document.querySelector('#post-slug');
  const gpTitle = document.querySelector('.gp-title');
  const gpDesc = document.querySelector('.gp-desc');
  const gpUrl = document.querySelector('.gp-url');
  if (!gpTitle) return;
  if (titleEl) gpTitle.textContent = titleEl.value || 'Título da página';
  if (descEl) gpDesc.textContent = descEl.value || 'Descrição da página aparecerá aqui...';
  if (slugEl && gpUrl) gpUrl.textContent = `startcorretoradeseguros.com.br/blog/${slugEl.value || 'url-do-post'}`;
}

/* ── Admin: Image upload preview ── */
const imageUpload = document.querySelector('#image-upload');
const imagePreview = document.querySelector('.upload-preview');
const uploadZone = document.querySelector('.upload-zone');
if (imageUpload && imagePreview) {
  imageUpload.addEventListener('change', e => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      imagePreview.src = ev.target.result;
      imagePreview.style.display = 'block';
    };
    reader.readAsDataURL(file);
  });
  if (uploadZone) {
    uploadZone.addEventListener('click', () => imageUpload.click());
    uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.style.borderColor = 'var(--primary)'; });
    uploadZone.addEventListener('dragleave', () => { uploadZone.style.borderColor = ''; });
    uploadZone.addEventListener('drop', e => {
      e.preventDefault();
      uploadZone.style.borderColor = '';
      imageUpload.files = e.dataTransfer.files;
      imageUpload.dispatchEvent(new Event('change'));
    });
  }
}

/* ── Admin: Status radio / schedule fields ── */
document.querySelectorAll('.status-radio input').forEach(r => {
  r.addEventListener('change', () => {
    const sched = document.querySelector('.schedule-fields');
    if (sched) sched.classList.toggle('visible', r.value === 'agendar');
  });
});

/* ── Admin: Save to localStorage ── */
const saveBtn = document.querySelector('#btn-save-draft');
if (saveBtn) {
  saveBtn.addEventListener('click', () => {
    const data = {
      title: document.querySelector('#post-title')?.value || '',
      slug: document.querySelector('#post-slug')?.value || '',
      metaTitle: document.querySelector('#meta-title')?.value || '',
      metaDesc: document.querySelector('#meta-desc')?.value || '',
      keyword: document.querySelector('#focus-kw')?.value || '',
      category: document.querySelector('#post-cat')?.value || '',
      savedAt: new Date().toISOString()
    };
    const drafts = JSON.parse(localStorage.getItem('sc_drafts') || '[]');
    const idx = drafts.findIndex(d => d.slug === data.slug);
    if (idx >= 0) drafts[idx] = data; else drafts.push(data);
    localStorage.setItem('sc_drafts', JSON.stringify(drafts));
    saveBtn.textContent = '✓ Salvo!';
    setTimeout(() => saveBtn.textContent = 'Salvar Rascunho', 2000);
  });
}

/* ── Admin: Calendar ── */
const calGrid = document.querySelector('.cal-grid-body');
const calTitle = document.querySelector('#cal-title');
if (calGrid && calTitle) {
  let currentDate = new Date();

  const scheduledPosts = JSON.parse(localStorage.getItem('sc_scheduled') || '[]');

  function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const months = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];
    calTitle.textContent = `${months[month]} ${year}`;
    calGrid.innerHTML = '';
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const today = new Date();
    for (let i = 0; i < firstDay; i++) {
      const el = document.createElement('div');
      el.className = 'cal-day empty';
      calGrid.appendChild(el);
    }
    for (let d = 1; d <= daysInMonth; d++) {
      const el = document.createElement('div');
      el.className = 'cal-day';
      if (today.getDate() === d && today.getMonth() === month && today.getFullYear() === year) el.classList.add('today');
      const dateStr = `${year}-${String(month+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
      const posts = scheduledPosts.filter(p => p.date === dateStr);
      el.innerHTML = `<div class="cal-day-num">${d}</div>` + posts.map(p => `<div class="cal-post-dot"></div><div class="cal-post-label">${p.title}</div>`).join('');
      el.addEventListener('click', () => {
        const title = prompt(`Agendar post para ${d}/${month+1}/${year}:`);
        if (title) {
          scheduledPosts.push({ date: dateStr, title });
          localStorage.setItem('sc_scheduled', JSON.stringify(scheduledPosts));
          renderCalendar();
        }
      });
      calGrid.appendChild(el);
    }
  }

  document.querySelector('#cal-prev')?.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
  });
  document.querySelector('#cal-next')?.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
  });

  renderCalendar();
}

/* ── Admin: KW filter ── */
document.querySelectorAll('.kw-filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.kw-filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    document.querySelectorAll('.kw-row').forEach(row => {
      if (filter === 'todos') {
        row.style.display = '';
      } else {
        const matches = row.dataset.intencao === filter || row.dataset.prioridade === filter;
        row.style.display = matches ? '' : 'none';
      }
    });
  });
});

/* ── Admin: Posts filter ── */
document.querySelectorAll('.posts-filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.posts-filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    document.querySelectorAll('.post-row').forEach(row => {
      if (filter === 'todos') row.style.display = '';
      else row.style.display = row.dataset.status === filter ? '' : 'none';
    });
  });
});
