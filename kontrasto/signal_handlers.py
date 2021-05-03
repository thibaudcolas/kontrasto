from django.db.models.signals import pre_save

from wagtail.images import get_image_model

from .willow_operations import pillow_dominant


def pre_save_image_dominant_color(instance, **kwargs):
    if not instance.has_dominant_color():
        instance.set_dominant_color(pillow_dominant(instance))


def register_signal_handlers():
    Image = get_image_model()
    # Rendition = Image.get_rendition_model()

    pre_save.connect(pre_save_image_dominant_color, sender=Image)
