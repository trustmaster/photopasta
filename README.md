# PhotoPasta 📸🍝

_Photo feed, your own way_

PhotoPasta helps you create beautiful self-hosted photo blogs. No media platforms, no ads, no garbage. You build it, you own it. Open source, based on widespread network protocols and existing web infrastructure.

## Uno, due, tre, pronto!

1. Import photos from convenient sources:
    -   Google Photos
    -   iCloud Shared Albums
    -   Local files
2. Create posts with a static site generator:
    -   Hugo
3. Host it anywhere, e.g.:
    -   Netlify
    -   CloudFlare
    -   any web hosting
4. Share it with the world via RSS feeds

## Demo

Demo website built with Hugo, PhotoPasta and Google Photos: [Photo Stories by Vladimir Sibirov](https://photos.kodigy.com).

## Ingredients

Currently PhotoPasta provides the following components that can be used independently to your liking:

-   Browser extensions to copy & paste photos from your Google Photos albums as Markdown shortcodes:
    -   Chrome Extension
    -   Firefox Addon
-   A tool that imports iCloud Shared Album to local directory and generates Markdown ready to be used in your next post
-   Custom shortcodes for [Hugo site generator](https://gohugo.io) to insert photos and turn your posts into beautiful galleries
-   Custom Hugo RSS template that enables your visitors to subscribe to all of your new posts and get them instantly with their favorite RSS reader app

## Getting started

### Starting your new site with Hugo

If you are new to Hugo, please follow [Quick start guide](https://gohugo.io/getting-started/quick-start/) on the Hugo website.

Once your site is up and running, you can proceed with setting it up to be used with photos content.

### Adding custom shortcodes, templates, and scripts to Hugo

#### Copy the files

Copy files from `hugo` directory of this project to your Hugo website folder.

#### Link CSS and JavaScript files

Add the following code to your theme's `layouts/partials/head.html`:

```html
<link rel="stylesheet" tyle="text/css" media="all" href="https://cdn.jsdelivr.net/npm/glightbox/dist/css/glightbox.min.css" />
<link rel="stylesheet" type="text/css" media="all" href="/css/gallery.css" />
```

Add the following code to your theme's `layout/partials/footer.html`:

```html
<script type="text/javascript" src="/js/gallery.js"></script>
<script type="text/javascript">
    const lightbox = GLightbox({
        selector: ".photo",
        width: "100vw",
        height: "auto",
        preload: false,
        loop: true,
    });
</script>
```

#### Adjust defaults if needed

You can adjust default CSS and JS files `static/css/gallery.css` and `static/js/gallery.js` to fit your website better. The setting variables are at the top of the files.

#### Copy the RSS template for full content feeds

By default Hugo generates RSS feeds with only the short summary of your posts with at most one image. If you want to let your visitors consume full content of your photo blog by subscribing to it via RSS, you will need to use a custom RSS template.

Copy `layouts/_default/rss.xml` from the `hugo` directory of this repo to your Hugo website folder. This template will be used to generate RSS feeds for your website. It is based on the default Hugo RSS template, but it includes full content of your posts instead of just the summary.

## Browser extension

### Installing the browser extension

Currently this step is only needed if you plan inserting content from Google Photos. You can install the extension from the official stores:

- Google Chrome users: _TODO: add link_
- **Firefox** users: [PhotoPasta Firefox Add-on](https://addons.mozilla.org/ru/firefox/addon/photopasta/)

Copying the links to Google Photos gives persistent links only if you use the extension while browsing the album as a guest. You will need to use a browser other than your primary one for that and stay logged out of your Google account, or you can use the same browser but in incognito mode.

If you are willing to use the incognito mode, an extra step is required to enable the extension in incognito mode. Here is how to do it:

- In Google chrome: open the extensions page using the URL , find the PhotoPasta extension, and enable "Allow in incognito" option.
- In Firefox: open the extensions page (about:addons), find the PhotoPasta extension, and enable "Run in Private Windows" option.

### Browser extension settings

If you click on the PhotoPasta extension icon (📷), it will open a Settings and Help dialog. The PhotoPasta extension has the following settings:

- **Create preview miniatures** - this option adds smaller downsized images for the photos that are actually pasted into the page to reduce the loading time. The original image is then opened when clicking on the preview thumbnail.
- **Optimize for High DPI displays** - this option improves drastically the quality of the preview miniatures on high DPI displays (which are used on a lot of modern devices like iPhone, flagship Android phones, Macbooks, 4k displays, etc.). The cost for this is that the images are roughly 2 times larger in size.
- **Preview width** - this is the default width for preview miniatures that are pasted as full-width images (fitting to the width of entire page). Set it to the maximum width of the content area on the website. The default value is 1200px. E.g. on my website it is 840px.
- **Row height for gallery** - for tiled galleries, height takes priority over width. This setting sets _approximate_ height of the images that you copy for the gallery.
- **Use captions** - inserts `caption` attribute for the photos using the description from Google Photos as its content. The caption attribute is both shown next to the photos in the full screen view as well as alternative text for screen readers.

## Adding content

### Inserting photos from Google Photo

Here is a step-by-step guide on how to insert photos from Google Photos into your post using PhotoPasta browser extension.

#### Prepare a shared album for your post

It is convenient to first create a shared album in Google Photos and add all the photos you want to use in your post to that album. This way you can easily access all the photos you need in one place. It also maes sure PhotoPasta and your site visitors will have proper access to the photo files.

Create a new Album in Google Photos. Then browse or search your photo feed, select photos for your album, click add (+) -> Album, and select the album you just created.

#### Open the shared album in a guest session

Once you want to proceed to pasting the photos into your post, open the album, click the share button (three dots connected with two edges), the click "Copy link" button, and copy the link. You will need to paste this link into the other browser or incognito brower window.

#### Paste photos into your post

Click on the photo you want to add to your post to open it in a single view mode. The right click on the photo. You will see a "📷 PhotoPasta" item there. Select it with a "Copy Photo Markdown" sub-item. This copies full-width photo for your page. Then you just paste it in your post.

Once you paste the photo, it is recommended to change the content of the `caption` attribute to something that describes the photo.

You might get a "The page is out of focus. Click on the page and try again" error message sometimes. It happens because your device is focused on another window or application. Just click on the photo so that the browser gets focus and try again.

#### Creating tiled galleries in your post

Apart from full-width photos, you can also create tiled galleries.

First, add a gallery shortcode to your post where you want to add the tiled gallery:

```
{{<gallery>}}

PASTE PHOTO SHORTCODES HERE

{{</gallery>}}
```

Tiles in the gallery don't need to be full-width. You can use any number of tiles in a row. The gallery will automatically adjust to the width of the screen. Approximate row width is configured in the PhotoPasta extension settings (click the PhotoPasta extension icon in the browser to open them).

To add a photo to the gallery, right click on it and select "📷 PhotoPasta" -> "Copy Markdown for Gallery item". Then paste it between the `{{<gallery>}}` and `{{</gallery>}}` shortcodes. Repeat it for all the photos you want to add to the gallery.

You can add more than one gallery to your post. Just add another `{{<gallery>}}` shortcode and paste the photos for it. It is recommended to use a combination of galleries and full-width posts interspersed with text to make your post more readable.

### Importing photos from Apple iCloud Shared Albums

_TODO_

### Using the shortcodes in Hugo

_TODO_

## Hosting your website

Your Photo blog can be hosted anywhere. Hugo docs have a set of example guides of hosting and deploying a Hugo-generated website to the popular platforms: [Hosting & Deployment](https://gohugo.io/hosting-and-deployment/).

## Using RSS to subscribe to content

_TODO_

---

## Credits

The gallery component makes use of the beautiful [GLightbox](https://github.com/biati-digital/glightbox) by Biati Digital.

The tools were inspired by the following prior work:

- [Building Google Photos Web UI](https://medium.com/google-design/google-photos-45b714dfbed1)
- [Flexbin](https://github.com/guoyunhe/flexbin)
- [Hugo Shortcode Gallery](https://github.com/mfg92/hugo-shortcode-gallery)
- [ICloud Shared Album](https://github.com/ghostops/ICloud-Shared-Album)
- [Justified Image Grid only with CSS & HTML](https://ehtmlu.com/blog/justified-image-grid-only-with-css-html)

Thanks to the authors of these libraries, tools, and articles.
