// <SETTINGS>
const rateLimitInterval = 200; // ms interval between image loading
const resizeDebounceDelay = 2000; // ms debouncing for window resize
// </SETTINGS>

function setGalleryContainerSize() {
        const imgs = document.querySelectorAll(".gallery a img");
        imgs.forEach((img) => {
            const width = img.getAttribute("width");
            const height = img.getAttribute("height");
            img.parentElement.style.setProperty("--width", width);
            img.parentElement.style.setProperty("--height", height);
        });
    }

function getViewportWidth() {
    return Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
}

function replaceDimensionsInUrl(url, width) {
    const match = url.match(/=w(\d+)-h(\d+)/);
    if (match) {
        const originalWidth = parseInt(match[1]);
        const originalHeight = parseInt(match[2]);
        const aspectRatio = originalWidth / originalHeight;
        const newHeight = Math.round(width / aspectRatio);
        return url.replace(/=w(\d+)-h(\d+)/, '=w' + width + '-h' + newHeight);
    }
    return url;
}

function adjustImagesToViewport(className) {
    const viewportWidth = getViewportWidth();
    const images = document.querySelectorAll(`img.${className}`);
    Array.from(images).forEach(function(img) {
        const url = img.src;
        const newUrl = replaceDimensionsInUrl(url, viewportWidth);
        const aspectRatio = img.naturalWidth / img.naturalHeight;
        img.src = newUrl;
        img.width = viewportWidth;
        img.height = Math.round(viewportWidth / aspectRatio);
    });
}

function adjustLinksToViewport(className) {
    let viewportWidth = getViewportWidth();
    const links = document.querySelectorAll(`a.${className}`);
    Array.from(links).forEach((link) => {
        const url = link.href;
        // Load images in 2x viewport width by default to support a bit of zoom on mobile
        if (link.dataset.width) {
            const width = parseInt(link.dataset.width, 10);
            if (2*viewportWidth < width) {
                viewportWidth = 2*viewportWidth;
            }
        }
        const newUrl = replaceDimensionsInUrl(url, viewportWidth);
        link.href = newUrl;
    });
}

function loadImageDeferred(img, delay) {
    if (!('src' in img.dataset)) {
        return;
    }
    setTimeout(() => {
        img.src = img.dataset.src;
    }, delay);
}

function fadeInOnImageLoad() {
    const imgs = document.querySelectorAll('img.thumb');
    Array.from(imgs).forEach((img) => {
        img.addEventListener('load', (e) => {
            img.classList.add('fade-in');
            setTimeout(() => {
                img.classList.add('loaded');
            }, 2000);
        });
    });
}

function getElementDistanceFromViewport(element) {
    const rect = element.getBoundingClientRect();
    return Math.abs(rect.top);
}

function loadAllImagesProgressively() {
    const imgs = document.querySelectorAll("img[data-src^='https://lh3.googleusercontent.com']");
    // Sort imgs by distance from viewport
    const sortedImgs = Array.from(imgs).sort((a, b) => {
        return getElementDistanceFromViewport(a) - getElementDistanceFromViewport(b);
    });
    let delay = 0;
    sortedImgs.forEach((img) => {
        loadImageDeferred(img, delay);
        delay += rateLimitInterval;
    });
}

// Adjust linked image sizes to the viewport on window resize
let resizeDebounceTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeDebounceTimeout);
    resizeDebounceTimeout = setTimeout(() => {
        adjustLinksToViewport('photo');
    }, resizeDebounceDelay);
});

// Adjust right away
(function() {
    setGalleryContainerSize();
    // Wait for scroll to be over, then load images with throttling based on
    // distance from current viewport
    setTimeout(() => {
        fadeInOnImageLoad();
        loadAllImagesProgressively();
        adjustLinksToViewport('photo');
    }, 200);
})();
