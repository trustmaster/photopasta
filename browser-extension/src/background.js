const browser = chrome || browser;

function toggleIcons(mode) {
    if (mode === 'dark') {
        browser.action.setIcon({
            path: {
                16: 'images/icon-16-dark.png',
                24: 'images/icon-24-dark.png',
                32: 'images/icon-32-dark.png',
                48: 'images/icon-48-dark.png',
                128: 'images/icon-128-dark.png',
            }
        });
    } else {
        browser.action.setIcon({
            path: {
                16: 'images/icon-16.png',
                24: 'images/icon-24.png',
                32: 'images/icon-32.png',
                48: 'images/icon-48.png',
                128: 'images/icon-128.png',
            }
        });
    }
}

// var scriptsInjected = true;
// function injectContentScripts(tabId, callback) {
//     browser.scripting.insertCSS({
//         target: {tabId},
//         files: ['content.css']
//     });
//     browser.scripting.executeScript({
//         target: {tabId},
//         files: ['content.js']
//     }, callback);
//     scriptsInjected = true;
// }

function handleContextMenuClick(info, tab) {
    // if (!scriptsInjected) {
    //     injectContentScripts(tab.id, () => {
    //         browser.tabs.sendMessage(tab.id, {menuInfo: info});
    //     });
    browser.tabs.sendMessage(tab.id, { menuInfo: info });
}

function registerContextMenu() {
    browser.contextMenus.create({
        title: "Copy Photo Markdown",
        contexts: ["image"],
        id: 'single-image',
    });

    browser.contextMenus.create({
        title: "Copy Markdown for Gallery item",
        contexts: ["image"],
        id: 'single-image-gal',
    });

    // browser.contextMenus.create({
    //     title: "Copy Markdown for all available images",
    //     contexts: ["image"],
    //     id: 'all-images',
    // });
}

browser.contextMenus.onClicked.addListener(handleContextMenuClick);

browser.runtime.onInstalled.addListener(registerContextMenu);

browser.runtime.onMessage.addListener((request) => {
    if (request.theme) {
        toggleIcons(request.theme);
    }
});
