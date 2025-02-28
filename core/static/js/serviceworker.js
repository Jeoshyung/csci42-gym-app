self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('django-pwa-cache').then((cache) => {
            return cache.addAll([
                '/',
                '/static/images/icon.png',
                '/static/js/serviceworker.js'
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
