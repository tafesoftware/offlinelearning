const CACHE_NAME = 'offline-lms-v1.0.5';
const ASSETS_TO_CACHE = [
  '/',
  '/auth/login',
  '/student/dashboard',
  '/student/offline-center',
  '/static/css/app.css',
  '/static/js/app.js',
  '/static/js/i18n.js',
  '/static/js/db.js',
  '/static/js/sync.js',
  '/static/js/quiz.js',
  '/static/manifest.json',
  '/static/icons/ministry-of-education.png',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png'
];

// Install Event: Pre-cache core application shell
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Beacon SW] Precaching offline application shell');
      return cache.addAll(ASSETS_TO_CACHE).catch((err) => {
        console.warn('[Beacon SW] Pre-cache non-fatal warning:', err);
      });
    })
  );
});

// Activate Event: Clean up outdated caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[Beacon SW] Removing old cache version:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event: Network-first for pages, Cache-first for static assets
self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);

  // Skip non-GET requests (e.g. POST to outbox will be handled via client IndexedDB)
  if (event.request.method !== 'GET') {
    return;
  }

  // 1. Static assets: Cache First, fallback to Network
  if (requestUrl.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, responseClone));
          }
          return networkResponse;
        });
      })
    );
    return;
  }

  // 2. HTML navigation requests: Network First, fallback to Cache
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        // Cache successful responses for offline access
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, responseClone));
        }
        return networkResponse;
      })
      .catch(async () => {
        // Device is offline: try matching cached URL
        const cachedMatch = await caches.match(event.request);
        if (cachedMatch) {
          return cachedMatch;
        }
        // If navigating to a page not cached, show offline hub
        if (event.request.mode === 'navigate') {
          const fallback = await caches.match('/student/offline-center');
          if (fallback) return fallback;
        }
        return new Response(
          '<h1 style="font-family:sans-serif;text-align:center;margin-top:20vh;">You are offline</h1><p style="text-align:center;">Please check your downloaded lessons in Beacon Offline Hub.</p>',
          { headers: { 'Content-Type': 'text/html' } }
        );
      })
  );
});

// Background Sync listener if supported
self.addEventListener('sync', (event) => {
  if (event.tag === 'beacon-sync-outbox') {
    event.waitUntil(
      self.clients.matchAll().then((clients) => {
        clients.forEach((client) => {
          client.postMessage({ type: 'TRIGGER_AUTO_SYNC' });
        });
      })
    );
  }
});
