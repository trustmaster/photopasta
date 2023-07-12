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

### Installing the browser extension

Currently this step is only needed if you plan inserting content from Google Photos. You can install the extension from the official stores:

- Google Chrome users: _TODO: add link_
- Firefox users: _TODO: add link_

## Adding content

### Inserting photos from Google Photo

_TODO_

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
