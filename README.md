# [Kontrasto](https://kontrasto.netlify.app) <img src="https://raw.githubusercontent.com/thibaudcolas/kontrasto/main/.github/kontrasto-logo.svg?sanitize=true" width="100" height="100" align="right" alt="">

[![PyPI](https://img.shields.io/pypi/v/kontrasto.svg)](https://pypi.org/project/kontrasto/) [![npm](https://img.shields.io/npm/v/kontrasto.svg)](https://www.npmjs.com/package/kontrasto) [![PyPI downloads](https://img.shields.io/pypi/dm/kontrasto.svg)](https://pypi.org/project/kontrasto/) [![Build status](https://github.com/thibaudcolas/kontrasto/workflows/CI/badge.svg)](https://github.com/thibaudcolas/kontrasto/actions) [![Coverage Status](https://coveralls.io/repos/github/thibaudcolas/kontrasto/badge.svg?branch=main)](https://coveralls.io/github/thibaudcolas/kontrasto?branch=main) [![Total alerts](https://img.shields.io/lgtm/alerts/g/thibaudcolas/kontrasto.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/thibaudcolas/kontrasto/alerts/) [![Netlify Status](https://api.netlify.com/api/v1/badges/e7517da4-87da-46d4-856e-13d5c2969908/deploy-status)](https://app.netlify.com/sites/kontrasto/deploys)

[![🎨 Automated color contrast for text over images](https://raw.githubusercontent.com/thibaudcolas/kontrasto/main/.github/repository-social-media.jpg)](https://kontrasto.netlify.app)

## Why we need this

Kontrasto is a dual Python and JavaScript library which analyses instances of text over images, and transforms the text to make it more readable and have a [higher contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) against the background.

Using Kontrasto both server-side and client-side gives the best results: server-side processing means users will have the best possible styles as the page loads, while client-side processing can refine the result based on the final position of the text over the image.

Here is a demo, over different areas of an image, with different methods of dominant color extraction and contrast ratio calculation:

[![Snow-covered landscape with snow-covered trees, blue-white sky, and a snow-covered radio tower on the horizon](https://raw.githubusercontent.com/thibaudcolas/kontrasto/main/.github/kontrasto-demo-readme.jpg)](https://kontrasto.netlify.app/)

Check out our [live demo](https://kontrasto.netlify.app/) for other examples.

## Usage in Python

kontrasto is available on [PyPI](https://pypi.org/project/kontrasto/).

```bash
# Assuming you’re using Python 3.6+,
pip install kontrasto
```

## Usage in JavaScript

kontrasto is available on [npm](https://www.npmjs.com/package/kontrasto).

```bash
npm install kontrasto
```

## Contributing

See anything you like in here? Anything missing? We welcome all support, whether on bug reports, feature requests, code, design, reviews, tests, documentation, and more. Please have a look at our [contribution guidelines](CONTRIBUTING.md).

If you just want to set up the project on your own computer, the contribution guidelines also contain all of the setup commands.

## Credits

Image credit: [FxEmojis](https://github.com/mozilla/fxemoji). [Test templates](tests/README.md) extracted from third-party projects. Website hosted by [Netlify](https://www.netlify.com/).

View the full list of [contributors](https://github.com/thibaudcolas/kontrasto/graphs/contributors). [MIT](LICENSE) licensed. Website content available as [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/).
