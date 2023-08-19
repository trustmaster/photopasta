const browser = chrome || browser;

function showToast(message, warning = false) {
    const toast = document.createElement('div');
    toast.style = "display:none";
    toast.classList.add('hcg-toast');
    if (warning) {
        toast.classList.add('hcg-toast-warning');
    }
    toast.innerText = message;
    document.body.appendChild(toast);
    // Fade in the toast
    setTimeout(() => {
        toast.style = "display:block";
    }, 100);
    // Fade out after a few seconds
    const fadeTime = warning ? 10000 : 5000;
    setTimeout(() => {
        toast.style = "display:none";
        toast.remove();
    }, fadeTime);
}

function getPlainUrl(url) {
    return url.substring(0, url.indexOf('='));
}

function trimLeadingDash(str) {
    if (str.indexOf('-') === 0) {
        return str.substring(1);
    }
    return str;
}

function getSizePostfix(width, height) {
    return `-w${width}-h${height}`;
}

function getScalePostfix() {
    return '-s';
}

function getNoOptimizePostfix() {
    return '-no';
}

function findAllGooglePhotoImages() {
    const containers = document.querySelectorAll('c-wiz[data-media-key]');

    let uniqueKeys = [];
    return Array.from(containers).map(container => {
        if (uniqueKeys.includes(container.dataset.mediaKey)) {
            return;
        }
        const img = container.querySelector('div img[aria-label]');
        return {
            src: getPlainUrl(img.src),
            label: img.getAttribute('aria-label'),
            width: parseInt(container.dataset.width, 10),
            height: parseInt(container.dataset.height, 10),
            aspectRatio: parseInt(container.dataset.width, 10) / parseInt(container.dataset.height, 10)
        }
    });
}

function findImageBySrc(srcUrl) {
    const plainUrl = getPlainUrl(srcUrl);
    const images = document.querySelectorAll(`c-wiz[data-media-key] img[src^="${plainUrl}"]:not([aria-hidden])`);
    if (images.length === 0) {
        return null;
    }
    const img = images[0];

    const container = img.closest('c-wiz[data-media-key]');
    if (!container) {
        return null;
    }

    return {
        src: plainUrl,
        label: img.getAttribute('aria-label'),
        width: parseInt(container.dataset.width, 10),
        height: parseInt(container.dataset.height, 10),
        aspectRatio: parseInt(container.dataset.width, 10) / parseInt(container.dataset.height, 10)
    }
}

function getOptions() {
    return browser.storage.sync.get({
        // maxWidth: 8000,
        useThumb: true,
        thumbHDPI: true,
        thumbWidth: 1200,
        rowHeight: 240,
        useCaption: true,
    });
}

function generatePhotoShortcode(image, options, isGalleryRow = false) {
    let src = image.src;
    let caption = '';
    let thumb = '';
    let width = '';
    let height = '';
    const originalWidth = image.width;
    const originalHeight = image.height;
    const originalRatio = image.aspectRatio;

    if (options.useThumb) {
        let thumbWidth = 0;
        let thumbHeight = 0;

        if (isGalleryRow && options.rowHeight && options.rowHeight > 0) {
            // For gallery rows, we fit the image into the row height
            thumbHeight = options.rowHeight;
            thumbWidth = Math.round(thumbHeight * originalRatio);
        } else if (options.thumbWidth && options.thumbWidth > 0) {
            // By default, thumbnail has width priority
            thumbWidth = options.thumbWidth;
            thumbHeight = Math.round(thumbWidth / originalRatio);
        }

        // Gallery row height can be exceeded by up to 50%
        const scaleFactor = isGalleryRow ? 1.5 : 1;
        const highDPIFactor = 2;
        let scale = scaleFactor;
        if (options.thumbHDPI) {
            scale = scale * highDPIFactor;
        }
        let imgWidth = scale * thumbWidth;
        let imgHeight = scale * thumbHeight;

        if (imgWidth > originalWidth) {
            // Sould never exceed original size
            imgWidth = originalWidth;
            imgHeight = originalHeight;
        }

        let postfix = getSizePostfix(imgWidth, imgHeight);
        postfix += getScalePostfix();
        postfix = trimLeadingDash(postfix);
        thumb = ` thumb="${src}=${postfix}"`;

        width = ` width="${thumbWidth}"`;
        height = ` height="${thumbHeight}"`;
    }

    if (options.useCaption && image.label) {
        caption = ` caption="${image.label}"`;
    }

    let srcPostfix = getSizePostfix(originalWidth, originalHeight);
    // if (options.maxWidth && options.maxWidth > 0 && originalWidth > options.maxWidth) {
    //     // Scale down the source image if it exceeds the max width
    //     const scaleRatio = options.maxWidth / originalWidth;
    //     const scaledWidth = Math.round(originalWidth * scaleRatio);
    //     const scaledHeight = Math.round(originalHeight * scaleRatio);
    //     srcPostfix = getSizePostfix(scaledWidth, scaledHeight);
    //     srcPostfix += getScalePostfix();
    // } else if (options.maxWidth && options.maxWidth > 0 && originalWidth === 0) {
    //     // Use the preselected width with the image aspect ratio
    //     const scaledWidth = options.maxWidth;
    //     const scaledHeight = Math.round(scaledWidth / originalRatio);
    //     srcPostfix = getSizePostfix(scaledWidth, scaledHeight);
    //     srcPostfix += getScalePostfix();
    // } else {
    //     srcPostfix += getNoOptimizePostfix();
    // }
    srcPostfix += getNoOptimizePostfix();

    srcPostfix = trimLeadingDash(srcPostfix);
    return `{{<photo${caption} src="${src}=${srcPostfix}"${thumb}${width}${height} src-width="${originalWidth}" src-height="${originalHeight}" >}}`;
}

function copyToClipboard(text) {
    if (!document.hasFocus()) {
        showToast('⚠️ The page is out of focus. 👉 Click on the page and try again.', true);
        return;
    }

    navigator.clipboard.writeText(text).then(() => {
        showToast('Markdown copied to clipboard!');
    }).catch(err => {
        showToast(`⚠️ Failed to copy to clipboard: ${err} 👉 Click on the page and try again.`, true);
    });
}

function copyAllToMarkdown() {
    getOptions().then(options => {
        const images = findAllGooglePhotoImages();
        if (images.length === 0) {
            showToast('⚠️ No images found', true);
            return;
        }

        const shortcodes = images.map(image => {
            return generatePhotoShortcode(image, options);
        });

        const markdown = shortcodes.join('\n\n');
        copyToClipboard(markdown);
    }).catch(err => {
        showToast(`⚠️ Failed to get options: ${err}`, true);
    });
}

function copyImageToMarkdown(srcUrl, isGalleryRow = false) {
    let url = srcUrl;
    getOptions().then(options => {
        const image = findImageBySrc(url);
        if (image === null) {
            showToast('⚠️ Failed to find image', true);
            return;
        }
        const shortcode = generatePhotoShortcode(image, options, isGalleryRow);

        copyToClipboard(shortcode);
    }).catch(err => {
        showToast(`⚠️ Failed to get options: ${err}`, true);
    });
}

try {
    console.log('CONTENT');

    browser.runtime.onMessage.addListener((request) => {
        if (request.menuInfo) {
            if (request.menuInfo.menuItemId === 'all-images') {
                copyAllToMarkdown();
            } else if (request.menuInfo.menuItemId === 'single-image') {
                copyImageToMarkdown(request.menuInfo.srcUrl);
            } else if (request.menuInfo.menuItemId === 'single-image-gal') {
                copyImageToMarkdown(request.menuInfo.srcUrl, true);
            }
        }
    });
} catch (err) {
    showToast(`⚠️ Error: ${err}`, true);
}
