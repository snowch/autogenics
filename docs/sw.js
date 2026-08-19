const CACHE='heaviness-10569455';
const ASSETS=["./", "./index.html", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png", "./video/after-first.mp4", "./video/after-first-poster.jpg", "./video/brief-warmth.mp4", "./video/brief-warmth-poster.jpg", "./video/brief-heartbeat.mp4", "./video/brief-heartbeat-poster.jpg", "./video/brief-breathing.mp4", "./video/brief-breathing-poster.jpg", "./video/brief-solar.mp4", "./video/brief-solar-poster.jpg", "./video/brief-forehead.mp4", "./video/brief-forehead-poster.jpg", "./video/finished.mp4", "./video/finished-poster.jpg", "./audio/arm-heaviness-example.mp3", "./audio/at-heaviness-all.mp3", "./audio/at-warmth.mp3", "./audio/at-heartbeat.mp3", "./audio/at-breathing.mp3", "./audio/at-solar-plexus.mp3", "./audio/at-forehead.mp3"];
self.addEventListener('install',e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));
});
self.addEventListener('activate',e=>{
  e.waitUntil(caches.keys()
    .then(k=>Promise.all(k.filter(n=>n!==CACHE).map(n=>caches.delete(n))))
    .then(()=>self.clients.claim()));
});
/* Cache first: once installed the app must work with no signal at all. */
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  e.respondWith(caches.match(e.request,{ignoreSearch:true})
    .then(r=>r||fetch(e.request).then(res=>{
      const copy=res.clone();
      caches.open(CACHE).then(c=>c.put(e.request,copy)).catch(()=>{});
      return res;
    }).catch(()=>caches.match('./index.html'))));
});
