self.addEventListener('install', e => {
    self.skipWaiting();
  });
  
  self.addEventListener('activate', event => {
    event.waitUntil(clients.claim());
  });