const CACHE='heaviness-7795808';
const ASSETS=["./", "./index.html", "./manifest.webmanifest", "./video/intro.mp4", "./video/intro-poster.jpg", "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png", "./audio/explainer.mp3", "./audio/arm-heaviness-example.mp3", "./audio/arm-heaviness-example-2.mp3", "./audio/arm-heaviness-example-3.mp3", "./audio/at-warmth.mp3", "./audio/at-heartbeat.mp3", "./audio/at-breathing.mp3", "./audio/at-solar-plexus.mp3", "./audio/at-forehead.mp3"];
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
