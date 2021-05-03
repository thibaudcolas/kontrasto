from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.models import AbstractImage, AbstractRendition, Image, SourceImageIOError
from wagtail.images.edit_handlers import ImageChooserPanel

from kontrasto.willow_operations import pillow_dominant

# https://docs.wagtail.io/en/stable/advanced_topics/images/custom_image_model.html


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

                self.save(update_fields=['dominant_color'])

        return self.dominant_color


class Rendition(AbstractRendition):
    image = models.ForeignKey(
        "CustomImage", related_name="renditions", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class HomePage(Page):
    body = RichTextField(blank=True)
    test_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        ImageChooserPanel('test_image'),
    ]
