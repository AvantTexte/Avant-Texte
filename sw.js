const CACHE_NAME = 'liseur-v2-cache';
const ASSETS = [
    './',
    './index.html',
    './styles.css',
    './app.js',
    './datos/index.json'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
