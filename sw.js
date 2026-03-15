// YaroShop Service Worker v1.0
const CACHE = 'yaroshop-v2';
const STATIC = [
  '/',
  '/index.html',
  '/marketplace.html',
  '/vendors.html',
  '/shop.html',
  '/product.html',
  '/cart.html',
  '/tracking.html',
  '/services.html',
  '/login.html',
  '/register.html',
  '/404.html',
  '/about.html',
  '/deals.html',
  '/help.html',
  '/terms.html',
  '/privacy.html',
  '/assets/styles.css',
  '/assets/app.js',
  '/assets/logo.svg'
];

// Install: cache static assets
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(STATIC)).then(() => self.skipWaiting())
  );
});

// Activate: clean old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch: cache-first for static, network-first for API
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // Only handle same-origin GET requests
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;

  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        // Cache successful HTML/CSS/JS/SVG responses
        if (res.ok && (url.pathname.endsWith('.html') || url.pathname.endsWith('.css') || url.pathname.endsWith('.js') || url.pathname.endsWith('.svg'))) {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      }).catch(() => {
        // Offline fallback for navigation requests
        if (e.request.mode === 'navigate') {
          return caches.match('/index.html');
        }
      });
    })
  );
});
