const CACHE = 'circuit-rounds-d2fb1c5242';
const FILES = ["./", "index.html", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png"];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES.map(u => new Request(u, { cache: 'reload' })))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('circuit-rounds-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  if (new URL(e.request.url).pathname.includes('/lectures/')) return;  // audio: network or the app's own lecture cache
  if (e.request.mode === 'navigate') {
    const net = fetch(e.request, { cache: 'no-cache' }).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => Promise.all([c.put('index.html', copy.clone()), c.put('./', copy)])); }
      return res;
    });
    e.waitUntil(net.catch(() => {}));
    e.respondWith(new Promise(resolve => {
      let done = false; const fin = r => { if (!done && r) { done = true; resolve(r); } };
      const saved = () => caches.match('index.html').then(fin);
      const t = setTimeout(saved, 4000);
      net.then(r => { clearTimeout(t); r.ok ? fin(r) : saved().then(() => fin(r)); }).catch(() => { clearTimeout(t); saved().then(() => fin(Response.error())); });
    }));
    return;
  }
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(hit => {
    if (hit) return hit;
    return fetch(e.request).then(res => {
      if (res.ok && new URL(e.request.url).origin === location.origin) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
      return res;
    }).catch(() => caches.match('index.html'));
  }));
});
