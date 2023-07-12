const browser = chrome || browser;

function openTab(event) {
    const tabName = event.target.getAttribute("data-tab");

    const tabContents = document.getElementsByClassName("tab-content");
    Array.from(tabContents).forEach((tabContent) => {
        tabContent.style.display = "none";
    });

    const tabButtons = document.getElementsByClassName("tab-button");
    Array.from(tabButtons).forEach((tabButton) => {
        tabButton.className = tabButton.className.replace(" active", "");
    });

    document.getElementById(tabName).style.display = "block";
    event.currentTarget.className += " active";
};

const tabButtons = document.getElementsByClassName("tab-button");
Array.from(tabButtons).forEach((tabButton) => {
    tabButton.addEventListener("click", openTab);
});


function showStatus(text) {
    const status = document.getElementById('status');
    status.textContent = text;
    status.style = "display:block";
    setTimeout(() => {
        status.style = "display:none";
        status.textContent = '';
    }, 2000);
}

function loadOptions() {
    browser.storage.sync.get({
        // maxWidth: 8000,
        useThumb: true,
        thumbHDPI: true,
        thumbWidth: 1200,
        rowHeight: 240,
        useCaption: true,
    }).then((options) => {
        // document.getElementById('max-width').value = options.maxWidth;
        document.getElementById('use-thumb').checked = options.useThumb;
        document.getElementById('thumb-hdpi').checked = options.thumbHDPI;
        document.getElementById('thumb-width').value = options.thumbWidth;
        document.getElementById('row-height').value = options.rowHeight;
        document.getElementById('use-caption').checked = options.useCaption;
    });
}

function saveOptions() {
    // const maxWidth = document.getElementById('max-width').value;
    const useThumb = document.getElementById('use-thumb').checked;
    const thumbHDPI = document.getElementById('thumb-hdpi').checked;
    const thumbWidth = document.getElementById('thumb-width').value;
    const rowHeight = document.getElementById('row-height').value;
    const useCaption = document.getElementById('use-caption').checked;

    if (useThumb && thumbWidth == 0) {
        document.getElementById('use-thumb').checked = false;
        showStatus('[!] Thumbnail is required when using preview thumbnails');
        return;
    }

    browser.storage.sync.set({
        // maxWidth,
        useThumb,
        thumbHDPI,
        thumbWidth,
        rowHeight,
        useCaption,
    }).then(() => {
        showStatus('Options saved');
    });
}

document.addEventListener('DOMContentLoaded', loadOptions);
document.getElementById('save').addEventListener('click', saveOptions);
