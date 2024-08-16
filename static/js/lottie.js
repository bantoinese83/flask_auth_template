
// Initialize Lottie Animations
let lottie = window.bodymovin;
lottie.loadAnimation({
    container: document.getElementById('welcome-animation'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://lottie.host/41896529-e63a-407b-b516-feca54160081/04048YZ4kP.json'
});

lottie.loadAnimation({
    container: document.getElementById('loading-animation'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://lottie.host/6db67e84-29ca-4df7-9aed-e918be35c04f/GUHZd8ZAiP.json'
});

lottie.loadAnimation({
    container: document.getElementById('success-animation'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://lottie.host/0d17b47d-7e01-4b7d-a8fb-f94b6c69dd48/jycOqQmo4J.json'
});

lottie.loadAnimation({
    container: document.getElementById('error-animation'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://lottie.host/caa8d9f2-7b02-4462-867d-4a5a1aa1a175/3HRdfJrk9m.json'
});

lottie.loadAnimation({
    container: document.getElementById('no-data-animation'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://lottie.host/aa234c54-eca8-4b61-a21c-83b5b1e82698/1EEUxyZ91a.json'
});