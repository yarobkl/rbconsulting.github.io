/* ================================================================
   ROMI OYO — index.js
   Interactions, chargement des données, formulaires
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initReveal();
  initBackTop();
  loadData();
});

// ===== NAVBAR =====
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const burger = document.getElementById('burger');
  const navLinks = document.getElementById('nav-links');

  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
    document.getElementById('back-top').classList.toggle('visible', window.scrollY > 300);
  });

  burger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    const spans = burger.querySelectorAll('span');
    burger.classList.toggle('active');
    if (burger.classList.contains('active')) {
      spans[0].style.transform = 'translateY(7px) rotate(45deg)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
    } else {
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    }
  });

  // Fermer menu au clic sur un lien
  navLinks.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      navLinks.classList.remove('open');
      burger.classList.remove('active');
      burger.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    });
  });
}

// ===== REVEAL AU SCROLL =====
function initReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); } });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}

// ===== BACK TO TOP =====
function initBackTop() {
  document.getElementById('back-top').addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ===== CHARGEMENT DES DONNÉES =====
async function loadData() {
  try {
    const res = await fetch('/api/load');
    if (!res.ok) throw new Error('API non disponible');
    const data = await res.json();
    renderAll(data);
  } catch {
    // Fallback : charger data.json directement
    try {
      const res = await fetch('/data.json');
      const data = await res.json();
      renderAll(data);
    } catch (e) {
      console.error('Impossible de charger les données', e);
    }
  }
  trackVisit();
  initForms();
}

function renderAll(data) {
  renderChiffres(data.chiffres || []);
  renderBiographie(data.biographie || {});
  renderTimeline(data.biographie?.parcours || []);
  renderActions(data.actions || []);
  renderFondation(data.fondation || {});
  renderAssemblee(data.assemblee || {});
  renderActualites(data.actualites || []);
  renderGalerie(data.galerie || []);
  renderTemoignages(data.temoignages || []);
}

// ===== CHIFFRES CLÉS =====
function renderChiffres(chiffres) {
  const grid = document.getElementById('chiffres-grid');
  if (!grid) return;
  grid.innerHTML = chiffres.map(c => `
    <div class="chiffre-item">
      <div class="chiffre-icone"><i class="fa-solid ${c.icone}"></i></div>
      <div class="chiffre-valeur" data-target="${c.valeur}">${c.valeur}</div>
      <div class="chiffre-label">${c.label}</div>
    </div>
  `).join('');
  animateCounters();
}

function animateCounters() {
  const counters = document.querySelectorAll('.chiffre-valeur');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target;
      const raw = el.dataset.target || el.textContent;
      const numMatch = raw.match(/[\d\s]+/);
      if (!numMatch) return;
      const target = parseInt(numMatch[0].replace(/\s/g, ''), 10);
      if (isNaN(target)) return;
      const suffix = raw.replace(/[\d\s]/g, '');
      let current = 0;
      const step = Math.ceil(target / 60);
      const timer = setInterval(() => {
        current = Math.min(current + step, target);
        el.textContent = current.toLocaleString('fr-FR') + suffix;
        if (current >= target) clearInterval(timer);
      }, 30);
      observer.unobserve(el);
    });
  }, { threshold: 0.5 });
  counters.forEach(c => observer.observe(c));
}

// ===== BIOGRAPHIE =====
function renderBiographie(bio) {
  const desc = document.getElementById('bio-description');
  if (desc) desc.textContent = bio.description || '';

  const photoEl = document.getElementById('bio-photo');
  if (photoEl && bio.photo) {
    photoEl.innerHTML = `<img src="${escHtml(bio.photo)}" alt="Photo officielle de Romi Oyo" />`;
  }
}

function renderTimeline(parcours) {
  const tl = document.getElementById('timeline');
  if (!tl) return;
  tl.innerHTML = parcours.map(p => `
    <div class="timeline-item">
      <div class="timeline-gauche">
        <span class="timeline-annee">${escHtml(p.annee)}</span>
        <div class="timeline-ligne"></div>
      </div>
      <div class="timeline-dot"></div>
      <div class="timeline-droite">
        <div class="timeline-titre">${escHtml(p.titre)}</div>
        <div class="timeline-desc">${escHtml(p.description)}</div>
      </div>
    </div>
  `).join('');
}

// ===== ACTIONS =====
function renderActions(actions) {
  const grid = document.getElementById('actions-grid');
  if (!grid) return;
  const badgeClass = {
    'Jeunesse': 'badge-jeunesse', 'Éducation': 'badge-education',
    'Social': 'badge-social', 'Sécurité': 'badge-securite',
    'Environnement': 'badge-environnement', 'Fondation': 'badge-fondation',
    'Sport': 'badge-sport'
  };
  grid.innerHTML = actions.map(a => `
    <div class="action-card">
      <div class="action-header">
        <div class="action-icone"><i class="fa-solid ${escHtml(a.icone)}"></i></div>
        <span class="action-badge ${badgeClass[a.badge] || 'badge-jeunesse'}">${escHtml(a.badge)}</span>
      </div>
      <div class="action-titre">${escHtml(a.titre)}</div>
      <div class="action-desc">${escHtml(a.description)}</div>
      <div class="action-date"><i class="fa-regular fa-calendar"></i> ${escHtml(a.date)}</div>
    </div>
  `).join('');
}

// ===== FONDATION =====
function renderFondation(fondation) {
  const desc = document.getElementById('fondation-description');
  if (desc) desc.textContent = fondation.description || '';

  const citation = document.getElementById('fondation-citation');
  if (citation) citation.textContent = `"${fondation.citation || ''}"`;

  const domaines = document.getElementById('fondation-domaines');
  if (domaines && fondation.domaines) {
    domaines.innerHTML = fondation.domaines.map(d => `
      <div class="fondation-domaine">
        <i class="fa-solid ${escHtml(d.icone)}"></i>
        <span>${escHtml(d.nom)}</span>
      </div>
    `).join('');
  }

  const bilan = document.getElementById('fondation-bilan');
  if (bilan && fondation.bilan) {
    bilan.innerHTML = fondation.bilan.map(b => `
      <div class="bilan-item">
        <div class="bilan-valeur">${escHtml(b.valeur)}</div>
        <div class="bilan-label">${escHtml(b.label)}</div>
      </div>
    `).join('');
  }
}

// ===== ASSEMBLÉE =====
function renderAssemblee(assemblee) {
  const rolesEl = document.getElementById('assemblee-roles');
  if (rolesEl && assemblee.roles) {
    rolesEl.innerHTML = assemblee.roles.map(r => `
      <div class="role-card">
        <div class="role-icone"><i class="fa-solid ${escHtml(r.icone)}"></i></div>
        <div>
          <div class="role-titre">${escHtml(r.titre)}</div>
          <div class="role-detail">${escHtml(r.detail)}</div>
        </div>
      </div>
    `).join('');
  }

  const engagementsEl = document.getElementById('engagements-list');
  if (engagementsEl && assemblee.engagements) {
    engagementsEl.innerHTML = assemblee.engagements.map(e => `
      <li class="engagement-item">
        <i class="fa-solid fa-circle-check check"></i>
        <span>${escHtml(e)}</span>
      </li>
    `).join('');
  }
}

// ===== ACTUALITÉS =====
function renderActualites(actualites) {
  const grid = document.getElementById('actu-grid');
  if (!grid) return;
  if (!actualites.length) {
    grid.innerHTML = '<p style="text-align:center;color:var(--gris);grid-column:1/-1">Aucune actualité pour le moment.</p>';
    return;
  }
  grid.innerHTML = actualites.map(a => `
    <div class="actu-card">
      <div class="actu-img"><i class="fa-solid fa-newspaper"></i></div>
      <div class="actu-corps">
        <div class="actu-meta">
          <span class="actu-categorie">${escHtml(a.categorie)}</span>
          <span class="actu-date">${escHtml(a.date)}</span>
        </div>
        <div class="actu-titre">${escHtml(a.titre)}</div>
        <div class="actu-resume">${escHtml(a.resume)}</div>
      </div>
    </div>
  `).join('');
}

// ===== GALERIE =====
function renderGalerie(galerie) {
  const grid = document.getElementById('galerie-grid');
  if (!grid) return;
  if (!galerie.length) return;
  grid.innerHTML = galerie.map(g => `
    <div class="galerie-item">
      <img src="${escHtml(g.url)}" alt="${escHtml(g.alt || 'Photo Romi Oyo')}" loading="lazy" />
    </div>
  `).join('');
}

// ===== TÉMOIGNAGES =====
function renderTemoignages(temoignages) {
  const grid = document.getElementById('temoignages-grid');
  if (!grid) return;
  grid.innerHTML = temoignages.map(t => `
    <div class="temoignage-card">
      <div class="temoignage-quote">"</div>
      <p class="temoignage-texte">${escHtml(t.texte)}</p>
      <div class="temoignage-auteur">
        <div class="temoignage-avatar"><i class="fa-solid fa-user"></i></div>
        <div>
          <div class="temoignage-nom">${escHtml(t.nom)}</div>
          <div class="temoignage-quartier">${escHtml(t.quartier)}</div>
        </div>
      </div>
    </div>
  `).join('');
}

// ===== FORMULAIRES =====
function initForms() {
  setupForm('form-audience',    'btn-audience',    'msg-audience',    '/api/audience');
  setupForm('form-reclamation', 'btn-reclamation', 'msg-reclamation', '/api/reclamation');
  setupForm('form-contact',     null,              'msg-contact',     '/api/contact');
}

function setupForm(formId, btnId, msgId, endpoint) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!validateForm(form)) return;

    const btn = btnId ? document.getElementById(btnId) : form.querySelector('button[type=submit]');
    const msgEl = document.getElementById(msgId);
    const originalText = btn ? btn.innerHTML : '';

    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Envoi en cours...'; }

    const body = Object.fromEntries(new FormData(form));

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const json = await res.json();

      if (res.ok && json.success) {
        showMsg(msgEl, 'success', json.message || 'Votre message a bien été envoyé. Merci !');
        form.reset();
      } else {
        showMsg(msgEl, 'error', json.error || 'Une erreur est survenue. Réessayez.');
      }
    } catch {
      showMsg(msgEl, 'error', 'Connexion impossible. Vérifiez votre connexion.');
    } finally {
      if (btn) { btn.disabled = false; btn.innerHTML = originalText; }
    }
  });
}

function validateForm(form) {
  let valid = true;
  form.querySelectorAll('[required]').forEach(field => {
    field.classList.remove('error');
    if (!field.value.trim()) {
      field.classList.add('error');
      valid = false;
    }
  });
  return valid;
}

function showMsg(el, type, text) {
  if (!el) return;
  el.className = `form-msg ${type}`;
  el.textContent = text;
  el.style.display = 'block';
  setTimeout(() => { el.style.display = 'none'; }, 6000);
}

// ===== COMPTEUR DE VISITES =====
async function trackVisit() {
  try {
    await fetch('/api/track-visit', { method: 'POST' });
  } catch {
    // Silencieux
  }
}

// ===== UTILITAIRE : Échapper HTML =====
function escHtml(str) {
  if (typeof str !== 'string') return str ?? '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
