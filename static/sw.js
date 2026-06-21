self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => clients.claim());
self.addEventListener('fetch', e => e.respondWith(fetch(e.request)));

// ── Notifications Web Push ──────────────────────────────────────────────
self.addEventListener('push', e => {
  let data = {};
  try { data = e.data ? e.data.json() : {}; } catch (err) { data = { body: (e.data && e.data.text()) || '' }; }
  const title = data.title || 'Qeerah';
  const options = {
    body: data.body || '',
    icon: data.icon || '/static/qeerah-logo.png',
    badge: data.badge || '/static/qeerah-logo.png',
    data: { url: data.url || '/app' },
    tag: data.tag || undefined,
  };
  e.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url) || '/app';
  e.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
      for (const c of list) {
        if (c.url.includes(url) && 'focus' in c) return c.focus();
      }
      return clients.openWindow ? clients.openWindow(url) : null;
    })
  );
});
