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

The simplest way to try it out is to use the command-line interface:

```bash
kontrasto --text '#00ff00' demo_images/blue-sky-cliffs.jpg
```

This will extract the image’s dominant color, and compare it against three text colors: white, black, and the provided #00ff00. Here is a sample result:

- Dominant color: `#4971a1` (https://whocanuse.com/?b=4971a1&c=&f=16)
- WCAG 2 contrast black: 4.16:1 (AA large only, https://whocanuse.com/?b=4971a1&c=000000&f=16)
- WCAG 2 contrast white: 5.05:1 (AA, AAA large, https://whocanuse.com/?b=4971a1&c=ffffff&f=16)
- WCAG 2 contrast text color: 3.68:1 (AA large only, https://whocanuse.com/?b=4971a1&c=00ff00&f=16)
- WCAG 3 contrast black: 29.158302335633827
- https://whocanuse.com/?b=4971a1&c=000000&f=16
- WCAG 3 contrast white: 82.7306051896947
- [(18, 400), (16, 500)]
- https://www.myndex.com/APCA/?BG=4971a1&TXT=ffffff
- https://whocanuse.com/?b=4971a1&c=ffffff&f=18
- https://whocanuse.com/?b=4971a1&c=ffffff&f=16
- WCAG 3 contrast text color: 60.98703767172198
- [(24, 400), (18, 500), (16, 600)]
- https://www.myndex.com/APCA/?BG=4971a1&TXT=00ff00
- https://whocanuse.com/?b=4971a1&c=00ff00&f=24
- https://whocanuse.com/?b=4971a1&c=00ff00&f=18
- https://whocanuse.com/?b=4971a1&c=00ff00&f=16&s=b

From there, we can move onto more serious use cases!

### Usage in vanilla Python

Import the low-level methods and enjoy:

```python
from kontrasto import wcag_2, wcag_3
from kontrasto.convert import to_hex
from kontrasto.contrast import get_dominant_color
from PIL import Image

def wcag_2_contrast_light_or_dark(
    image, light_color: str, dark_color: str
) -> Dict[str, str]:
    dominant = to_hex(get_dominant_color(image))
    light_contrast = wcag_2.wcag2_contrast(dominant, light_color)
    dark_contrast = wcag_2.wcag2_contrast(dominant, dark_color)
    lighter = light_contrast > dark_contrast
    return {
        "text_color": light_color if lighter else dark_color,
        "text_theme": "light" if lighter else "dark",
        "bg_color": dominant,
        "bg_theme": "dark" if lighter else "light",
    }

def wcag_3_contrast_light_or_dark(
    image, light_color: str, dark_color: str
) -> Dict[str, str]:
    dominant = to_hex(get_dominant_color(image))
    light_contrast = wcag_3.format_contrast(
        wcag_3.apca_contrast(dominant, light_color)
    )
    dark_contrast = wcag_3.format_contrast(
        wcag_3.apca_contrast(dominant, dark_color)
    )
    lighter = light_contrast > dark_contrast
    return {
        "text_color": light_color if lighter else dark_color,
        "text_theme": "light" if lighter else "dark",
        "bg_color": dominant,
        "bg_theme": "dark" if lighter else "light",
    }
```

### Usage in Wagtail

In Wagtail, using Kontrasto is much simpler:

- The result of dominant color extraction is cached, greatly improving performance.
- The above methods are directly available as template tags.

At least for now, this does mean using Kontrasto requires adding a field to a [custom image model](https://docs.wagtail.io/en/stable/advanced_topics/images/custom_image_model.html):

```python
from wagtail.images.models import (
    AbstractImage,
    AbstractRendition,
    SourceImageIOError,
)

from kontrasto.willow_operations import pillow_dominant

class CustomImage(AbstractImage):
    dominant_color = models.CharField(max_length=10, blank=True)

    admin_form_fields = Image.admin_form_fields

    def has_dominant_color(self) -> bool:
        return self.dominant_color

    def set_dominant_color(self, color: str) -> bool:
        self.dominant_color = color

    def get_dominant_color(self):
        if not self.has_dominant_color():
            with self.get_willow_image() as willow:
                try:
                    self.dominant_color = pillow_dominant(willow)
                except Exception as e:
                    # File not found
                    #
                    # Have to catch everything, because the exception
                    # depends on the file subclass, and therefore the
                    # storage being used.
                    raise SourceImageIOError(str(e))

                self.save(update_fields=["dominant_color"])

        return self.dominant_color


class Rendition(AbstractRendition):
    image = models.ForeignKey(
        "CustomImage", related_name="renditions", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
```

Add kontrasto to your installed apps. In your settings module:

```python
INSTALLED_APPS = [
    # ...
    # other apps
    "kontrasto",
]
```

Then, in templates:

```html
{% load kontrasto_tags %}

{% wcag_2_contrast_light_or_dark page.test_image "#ffffff" "#000000" as result
%} {% wcag_3_contrast_light_or_dark page.test_image "#ffffff" "#000000" as
result_3 %}
<div
  data-banner
  style="--kontrasto-text:{{ result_3.text_color }}; --kontrasto-bg:{{ result_3.bg_color }}99;"
>
  {% image page.test_image width-800 loading="lazy" data-banner-image="true" %}
  <p>
    <span class="kontrasto-text-bg" data-banner-text>{{ demo_text }}</span>
  </p>
</div>
```

This additionally relies on the following CSS, for the simplest integration with client-side processing:

```css
.kontrasto-text-bg {
  color: var(--kontrasto-text);
  background: var(--kontrasto-bg);
}
```

## Usage in JavaScript

kontrasto is available on [npm](https://www.npmjs.com/package/kontrasto) for client-side (browser) JavaScript. This option makes it possible to only extract the dominant color of images _where the text appears_, which leads to much better results. However, it has the caveat of executing in the users’ browser, which has a clear performance cost.

```bash
npm install kontrasto
```

Using it in JavaScript is slightly different.

### Vanilla JavaScript

Here is a basic vanilla JavaScript integration:

```js
import {
  wcag_2_contrast_light_or_dark,
  wcag_3_contrast_light_or_dark,
} from "kontrasto";

const banner = document.querySelector("[data-banner]");
const bannerImage = banner.querySelector("[data-banner-image]");
const bannerText = banner.querySelector("[data-banner-text]");

const contrast = wcag_3_contrast_light_or_dark(
  bannerImage,
  "#ffffff",
  "#000000",
  bannerText,
);
banner.style.setProperty("--kontrasto-bg", `${contrast.bg_color}99`);
banner.style.setProperty("--kontrasto-text", contrast.text_color);
```

This assumes an HTML structure like:

```html
{% wcag_2_contrast_light_or_dark page.test_image "#ffffff" "#000000" as result
%} {% wcag_3_contrast_light_or_dark page.test_image "#ffffff" "#000000" as
result_3 %}
<div
  data-banner
  style="--kontrasto-text:{{ result_3.text_color }}; --kontrasto-bg:{{ result_3.bg_color }}99;"
>
  {% image page.test_image width-800 loading="lazy" data-banner-image="true" %}
  <p>
    <span class="kontrasto-text-bg" data-banner-text>{{ demo_text }}</span>
  </p>
</div>
```

And CSS:

```css
.kontrasto-text-bg {
  color: var(--kontrasto-text);
  background: var(--kontrasto-bg);
}
```

Combined with the server-side integration, this makes it possible to deliver both the best possible performance, and the best possible text contrast enhancement.

#### Particular considerations

TODO

### React

TODO

## Contributing

See anything you like in here? Anything missing? We welcome all support, whether on bug reports, feature requests, code, design, reviews, tests, documentation, and more. Please have a look at our [contribution guidelines](CONTRIBUTING.md).

If you just want to set up the project on your own computer, the contribution guidelines also contain all of the setup commands.

## Credits

Image credit: [FxEmojis](https://github.com/mozilla/fxemoji). [Test templates](tests/README.md) extracted from third-party projects. Website hosted by [Netlify](https://www.netlify.com/).

View the full list of [contributors](https://github.com/thibaudcolas/kontrasto/graphs/contributors). [MIT](LICENSE) licensed. Website content available as [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/).
