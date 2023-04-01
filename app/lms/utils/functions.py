import datetime
import logging
from io import BytesIO

from django.core.files import File
from django.utils.html import strip_tags
from PIL import Image

from setup.models import School, SchoolSession

logger = logging.getLogger("system")


def get_errors_from_form(form):
    errors = []
    for field, er in form.errors.items():
        title = field.title().replace("_", " ")
        errors.append(f"{title}: {strip_tags(er)}<br>")
    return "".join(errors)


def make_model_key_value(obj):
    ignores = ["password"]
    data = {}
    for field in obj._meta.fields:
        if field.name in obj.__dict__ and field.name not in ignores:
            value = obj.__dict__[field.name]
            if isinstance(value, datetime.datetime) or isinstance(
                    value, datetime.date):
                value = value.strftime("%Y-%m-%d")
            data[field.name] = value
    return data


def crop_image_to_size(picture, filename=None, quality=50):
    if not picture: return None
    if not filename:
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    try:
        thumb_io = BytesIO()
        image = Image.open(picture)
        width, height = image.size
        (width, height) = (width / 2, height / 2)
        x, y = 206 // 2, 265 // 2
        image = image.crop([width - x, height - y, width + x, height + y])
        image.save(thumb_io, "jpeg", quality=quality)
        new_image = File(thumb_io, name=f"{filename}.jpg")
        return new_image
    except Exception as e:
        logger.error("Compressing Image: " + str(e))
    return picture


def get_current_session():
    return School.objects.first().current_session or SchoolSession.objects.all(
    ).order_by("-start_date").first()


def crop_image(image, filename=None, crop_data=None, quality=50):
    left, top = crop_data[0], crop_data[1]
    right, bottom = crop_data[2] + left, crop_data[3] + top
    if not image:
        return None
    if not filename:
        filename = datetime.now().strftime("%Y%m%d%H%M%S%f")
    try:
        img = Image.open(image)
        thumb_io = BytesIO()
        img = img.crop((left, top, right, bottom))
        img = img.convert('RGB')
        img.save(thumb_io, "png", quality=quality)
        new_image = File(thumb_io, name=f"{filename}.png")
        image.delete()
        return new_image
    except Exception as e:
        logger.error("Compressing Image: " + str(e))
    return image