/* ═══════════════════════════════════════════
   YAROSHOP — JavaScript Core
═══════════════════════════════════════════ */

'use strict';

/* ─── Navbar scroll effect ─── */
const navbar = document.getElementById('navbar');
if (navbar) {
  const onScroll = () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
}

/* ─── Mobile nav toggle ─── */
const navToggle = document.getElementById('navToggle');
const navMobile = document.getElementById('navMobile');
if (navToggle && navMobile) {
  navToggle.addEventListener('click', () => {
    navMobile.classList.toggle('open');
    const spans = navToggle.querySelectorAll('span');
    const isOpen = navMobile.classList.contains('open');
    if (isOpen) {
      spans[0].style.transform = 'translateY(7px) rotate(45deg)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
    } else {
      spans[0].style.transform = '';
      spans[1].style.opacity = '';
      spans[2].style.transform = '';
    }
  });
}

/* ─── Animated counters ─── */
function animateCounter(el) {
  const target = parseInt(el.dataset.count, 10);
  const duration = 2000;
  const start = performance.now();
  const fmt = (n) => n >= 1000 ? n.toLocaleString('fr-FR') : n;

  const step = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 4);
    const current = Math.round(eased * target);
    el.textContent = fmt(current);
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

const counters = document.querySelectorAll('.stat-number[data-count]');
if (counters.length) {
  const counterObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        animateCounter(e.target);
        counterObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(c => counterObs.observe(c));
}

/* ─── Scroll animations ─── */
const animatedEls = document.querySelectorAll('[data-aos]');
if (animatedEls.length) {
  const animObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.animationDelay = e.target.dataset.aosDelay || '0ms';
        e.target.classList.add('animated');
        animObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  animatedEls.forEach(el => {
    el.style.opacity = '0';
    animObs.observe(el);
  });
}

/* ─── How it Works tabs ─── */
const hiwTabs = document.querySelectorAll('.hiw-tab');
const hiwVendeur = document.getElementById('hiwVendeur');
const hiwAcheteur = document.getElementById('hiwAcheteur');

hiwTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    hiwTabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    if (tab.dataset.tab === 'vendeur') {
      hiwVendeur?.classList.remove('hidden');
      hiwAcheteur?.classList.add('hidden');
    } else {
      hiwVendeur?.classList.add('hidden');
      hiwAcheteur?.classList.remove('hidden');
    }
  });
});

/* ─── Product wishlist toggle ─── */
document.querySelectorAll('.product-wishlist').forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    btn.classList.toggle('active');
    const icon = btn.querySelector('svg path');
    if (icon) {
      if (btn.classList.contains('active')) {
        icon.setAttribute('fill', 'currentColor');
        showToast('Ajouté aux favoris ❤️');
      } else {
        icon.setAttribute('fill', 'none');
        showToast('Retiré des favoris');
      }
    }
  });
});

/* ─── Toast notification ─── */
function showToast(message, type = 'success') {
  const existing = document.querySelector('.yaroshop-toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'yaroshop-toast';
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed; bottom: 100px; right: 28px; z-index: 9999;
    background: ${type === 'error' ? 'var(--danger)' : 'var(--bg-card)'};
    border: 1px solid ${type === 'error' ? 'var(--danger)' : 'var(--border)'};
    color: var(--text); padding: 12px 20px;
    border-radius: 999px; font-size: 14px; font-weight: 600;
    box-shadow: var(--shadow-lg);
    transform: translateY(20px); opacity: 0;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
  `;
  document.body.appendChild(toast);
  requestAnimationFrame(() => {
    toast.style.transform = 'translateY(0)';
    toast.style.opacity = '1';
  });
  setTimeout(() => {
    toast.style.transform = 'translateY(20px)';
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

/* ─── Search functionality ─── */
const searchInputs = document.querySelectorAll('.nav-search input, .nav-mobile-search input');
searchInputs.forEach(input => {
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && input.value.trim()) {
      const q = encodeURIComponent(input.value.trim());
      window.location.href = `marketplace.html?q=${q}`;
    }
  });
});

const searchBtn = document.querySelector('.search-btn');
if (searchBtn) {
  searchBtn.addEventListener('click', () => {
    const input = document.querySelector('.nav-search input');
    if (input?.value.trim()) {
      window.location.href = `marketplace.html?q=${encodeURIComponent(input.value.trim())}`;
    }
  });
}

/* ─── Service type selection (services page) ─── */
document.querySelectorAll('.service-type-card').forEach(card => {
  card.addEventListener('click', () => {
    document.querySelectorAll('.service-type-card').forEach(c => c.classList.remove('active'));
    card.classList.add('active');
    const typeInput = document.getElementById('serviceType');
    if (typeInput) typeInput.value = card.dataset.type || card.querySelector('h3')?.textContent || '';
  });
});

/* ─── Dashboard chart rendering ─── */
function renderChart(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const data = [
    { label: 'Jan', value: 65 }, { label: 'Fév', value: 42 },
    { label: 'Mar', value: 87 }, { label: 'Avr', value: 53 },
    { label: 'Mai', value: 96 }, { label: 'Jun', value: 78 },
    { label: 'Jul', value: 110 }, { label: 'Aoû', value: 89 },
  ];
  const max = Math.max(...data.map(d => d.value));

  container.innerHTML = data.map(d => `
    <div class="chart-bar-group">
      <div class="chart-bar"
        style="height:${(d.value / max) * 140}px;background:linear-gradient(to top,var(--primary),var(--primary-light))"
        title="${d.value} ventes"></div>
      <span class="chart-bar-label">${d.label}</span>
    </div>
  `).join('');
}

renderChart('salesChart');

/* ─── Filter toggle (mobile) ─── */
const filterToggle = document.getElementById('filterToggle');
const sidebarEl = document.getElementById('sidebar');
if (filterToggle && sidebarEl) {
  filterToggle.addEventListener('click', () => {
    sidebarEl.style.display = sidebarEl.style.display === 'block' ? '' : 'block';
  });
}

/* ─── View toggle (grid/list) ─── */
document.querySelectorAll('.view-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.view-toggle').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const productsContainer = document.getElementById('productsContainer');
    if (!productsContainer) return;
    if (btn.dataset.view === 'list') {
      productsContainer.className = 'products-list';
    } else {
      productsContainer.className = 'products-grid-2';
    }
  });
});

/* ─── Admin actions ─── */
document.querySelectorAll('[data-action]').forEach(el => {
  el.addEventListener('click', (e) => {
    const action = el.dataset.action;
    const target = el.dataset.target;

    if (action === 'suspend') {
      if (confirm(`Suspendre l'utilisateur ${target}?`)) {
        showToast(`Utilisateur ${target} suspendu`);
        el.closest('tr')?.querySelector('.status-badge')?.classList.replace('status-active', 'status-suspended');
      }
    }
    if (action === 'approve') {
      showToast(`Boutique approuvée ✅`);
      el.closest('tr')?.querySelector('.status-badge')?.classList.replace('status-pending', 'status-active');
    }
    if (action === 'delete') {
      if (confirm('Supprimer définitivement?')) {
        el.closest('tr')?.remove();
        showToast('Supprimé', 'error');
      }
    }
  });
});

/* ─── Form validation ─── */
document.querySelectorAll('form[data-validate]').forEach(form => {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const required = form.querySelectorAll('[required]');
    let valid = true;

    required.forEach(field => {
      field.style.borderColor = '';
      if (!field.value.trim()) {
        field.style.borderColor = 'var(--danger)';
        valid = false;
      }
    });

    if (!valid) {
      showToast('Veuillez remplir tous les champs obligatoires', 'error');
      return;
    }

    const submitBtn = form.querySelector('[type="submit"]');
    if (submitBtn) {
      const original = submitBtn.textContent;
      submitBtn.textContent = 'Chargement...';
      submitBtn.disabled = true;
      setTimeout(() => {
        submitBtn.textContent = original;
        submitBtn.disabled = false;
        showToast(form.dataset.successMsg || 'Envoyé avec succès!');
      }, 1500);
    }
  });
});

/* ─── Lazy load images ─── */
if ('IntersectionObserver' in window) {
  const imgObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const img = e.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
        }
        imgObs.unobserve(img);
      }
    });
  });
  document.querySelectorAll('img[data-src]').forEach(img => imgObs.observe(img));
}

/* ─── Price range filter ─── */
const priceInputs = document.querySelectorAll('.price-input');
priceInputs.forEach(input => {
  input.addEventListener('input', debounce(() => {
    const min = document.querySelector('.price-input[name="min"]')?.value || 0;
    const max = document.querySelector('.price-input[name="max"]')?.value || 999999;
    filterProductsByPrice(parseInt(min), parseInt(max));
  }, 500));
});

function filterProductsByPrice(min, max) {
  document.querySelectorAll('.product-card').forEach(card => {
    const priceEl = card.querySelector('.price-current');
    if (!priceEl) return;
    const price = parseInt(priceEl.textContent.replace(/[^0-9]/g, ''));
    card.style.display = (price >= min && price <= max) ? '' : 'none';
  });
}

function debounce(fn, ms) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), ms); };
}

/* ─── WhatsApp order builder ─── */
function buildWhatsAppLink(phone, productName, price, shopName) {
  const message = `Bonjour ${shopName || ''}, je suis intéressé(e) par votre produit *${productName}* à ${price} FC sur YaroShop. Est-il disponible?`;
  return `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
}

/* ─── Category filter (marketplace) ─── */
const urlParams = new URLSearchParams(window.location.search);
const activeCategory = urlParams.get('cat');
if (activeCategory) {
  document.querySelectorAll('.filter-option').forEach(opt => {
    if (opt.dataset.category === activeCategory) opt.classList.add('active');
  });
}

/* ─── Keyboard nav ─── */
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    navMobile?.classList.remove('open');
  }
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    document.querySelector('.nav-search input')?.focus();
  }
});

/* ─── Performance: defer non-critical JS ─── */
window.addEventListener('load', () => {
  // Add smooth entrance animations
  document.body.style.opacity = '1';
  document.querySelectorAll('.product-card, .vendor-card, .category-card').forEach((el, i) => {
    el.style.animationDelay = `${i * 40}ms`;
    el.style.animation = 'fadeIn 0.5s cubic-bezier(0.4,0,0.2,1) both';
  });
});

// ── Pricing toggle ──────────────────────────────────────────────
function togglePricing() {
  const btn = document.getElementById("pricing-toggle");
  const monthlyLabel = document.getElementById("toggle-monthly");
  const annualLabel = document.getElementById("toggle-annual");
  const isAnnual = btn.classList.toggle("annual");
  monthlyLabel.classList.toggle("active", !isAnnual);
  annualLabel.classList.toggle("active", isAnnual);
  document.querySelectorAll(".price-amount").forEach(el => {
    el.textContent = isAnnual ? el.dataset.annual : el.dataset.monthly;
  });
}

// ── Enhanced Navbar: cart panel + profile dropdown ───────────────
(function initNavbar() {
  // Inject cart panel + overlay into every page
  const cartPanel = document.createElement('div');
  cartPanel.id = 'cartPanelOverlay';
  cartPanel.className = 'cart-panel-overlay';
  cartPanel.innerHTML = `
    <div class="cart-panel" id="cartPanel">
      <div class="cart-panel-header">
        <span class="cart-panel-title">Mon Panier <span id="cpCount" style="background:var(--primary);color:white;font-size:0.7rem;font-weight:800;padding:2px 8px;border-radius:999px;margin-left:6px">3</span></span>
        <button class="cart-panel-close" onclick="closeCartPanel()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>
      <div class="cart-panel-body">
        <div class="cart-panel-item">
          <div class="cart-panel-emoji">📱</div>
          <div class="cart-panel-info">
            <div class="cart-panel-name">Samsung Galaxy A54 5G</div>
            <div class="cart-panel-opts">Noir · 256Go</div>
            <div class="cart-panel-row">
              <span class="cart-panel-price">350 $</span>
              <span class="cart-panel-qty">× 1</span>
            </div>
          </div>
        </div>
        <div class="cart-panel-item">
          <div class="cart-panel-emoji">🎧</div>
          <div class="cart-panel-info">
            <div class="cart-panel-name">Écouteurs TWS Pro Max</div>
            <div class="cart-panel-opts">Blanc</div>
            <div class="cart-panel-row">
              <span class="cart-panel-price">58 $</span>
              <span class="cart-panel-qty">× 2</span>
            </div>
          </div>
        </div>
        <div class="cart-panel-item">
          <div class="cart-panel-emoji">👗</div>
          <div class="cart-panel-info">
            <div class="cart-panel-name">Robe Wax Africaine</div>
            <div class="cart-panel-opts">Taille M · Bleu royal</div>
            <div class="cart-panel-row">
              <span class="cart-panel-price">35 $</span>
              <span class="cart-panel-qty">× 1</span>
            </div>
          </div>
        </div>
      </div>
      <div class="cart-panel-footer">
        <div class="cart-panel-total">
          <span class="cart-panel-total-label">Total</span>
          <span class="cart-panel-total-val">448 $</span>
        </div>
        <a href="cart.html" class="btn-cart-checkout">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
          Finaliser la commande
        </a>
        <a href="cart.html" class="btn-cart-view">Voir le panier complet →</a>
      </div>
    </div>`;
  document.body.appendChild(cartPanel);
  cartPanel.addEventListener('click', e => { if (e.target === cartPanel) closeCartPanel(); });
})();

function openCartPanel() {
  document.getElementById('cartPanelOverlay').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeCartPanel() {
  document.getElementById('cartPanelOverlay').classList.remove('open');
  document.body.style.overflow = '';
}

function toggleProfileDropdown() {
  const dd = document.getElementById('profileDropdown');
  if (dd) dd.classList.toggle('open');
}

// Close dropdown on outside click
document.addEventListener('click', e => {
  const wrap = document.getElementById('profileDropdownWrap');
  if (wrap && !wrap.contains(e.target)) {
    const dd = document.getElementById('profileDropdown');
    if (dd) dd.classList.remove('open');
  }
});

// ── NavSearch global ────────────────────────────────────────────
function navSearch() {
  const inp = document.getElementById('navSearchInput');
  if (!inp) return;
  const q = inp.value.trim();
  if (q) window.location.href = 'search.html?q=' + encodeURIComponent(q);
}
if (document.getElementById('navSearchInput')) {
  document.getElementById('navSearchInput').addEventListener('keydown', e => {
    if (e.key === 'Enter') navSearch();
  });
}
