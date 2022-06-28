import json
import logging
from datetime import datetime, timedelta
from io import BytesIO

import redis
import requests
from django.conf import settings
from django.core.files import File
from PIL import Image
from redis.exceptions import ConnectionError

from accounts.models import Charge, Promotion, Store
from dashboard.serializers import ChargeSerializer, PromotionSerializer
from techstuff.settings.base import PAYHUB_SECRET_TOKEN

logger = logging.getLogger("django")
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


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


def reduce_image_size(picture,
                      filename=None,
                      size=(256, 256),
                      quality=50,
                      thumbnail=True):
    if not picture:
        return None
    if not filename:
        filename = datetime.now().strftime("%Y%m%d%H%M%S%f")
    try:
        img = Image.open(picture)
        thumb_io = BytesIO()
        if thumbnail and size:
            img.thumbnail(size, Image.ANTIALIAS)
        img = img.convert('RGB')
        img.save(thumb_io, "png", quality=quality)
        new_image = File(thumb_io, name=f"{filename}.png")
        picture.delete()
        return new_image
    except Exception as e:
        logger.error("Compressing Image: " + str(e))
    return picture


def make_disbursement(data):
    '''Make disbursement'''
    ENDPOINT = 'https://payhubghana.io/api/v1.0/credit_mobile_account/'
    headers = {
        "Authorization": f"Token {PAYHUB_SECRET_TOKEN}",
    }

    response = requests.post(ENDPOINT, data=data, headers=headers)
    response_data = response.json()
    return response_data


def get_transaction_status(transaction_id):
    ENDPOINT = 'https://payhubghana.io/api/v1.0/transaction_status'
    headers = {
        "Authorization": f"Token {PAYHUB_SECRET_TOKEN}",
    }
    params = {
        "transaction_id": transaction_id,
    }
    response = requests.get(ENDPOINT, params=params, headers=headers)
    response_data = response.json()
    return response_data


def get_charge_rate(store_id, category_id, amount):
    key = f"charges_{store_id}_{category_id}_{amount}"
    try:
        cache_data = redis_client.get(hash(key))
        if cache_data:
            return json.loads(cache_data.decode())
    except ConnectionError as e:
        logger.warning("Redis is not working")
        logger.error(str(e))

    logger.info(f"REDIS: missed key {key}")

    store = Store.objects.filter(id=store_id).first()
    charge = Charge.objects.filter(
        store=store,
        category_id=category_id,
        min_price__lte=amount,
        max_price__gte=amount).order_by("-id").first()
    if not (charge and store):
        try:
            redis_client.set(hash(key),
                             json.dumps({}).encode(),
                             ex=timedelta(days=30))
        except ConnectionError as e:
            logger.error(str(e))
        return None

    data = ChargeSerializer(charge).data
    try:
        redis_client.set(hash(key),
                         json.dumps(data).encode(),
                         ex=timedelta(days=30))
    except ConnectionError as e:
        logger.error(str(e))
    return data


def invalidate_charge_cache(store_id, category_id):
    keys = f"charges_{store_id}_{category_id}*"
    try:
        res = redis_client.delete(*keys)
        logger.info(f"REDIS: Deleted {res} keys")
    except ConnectionError as e:
        logger.error(str(e))


def get_promotion_rate(store_id, category_id, amount):
    key = f"promotions_{store_id}_{category_id}_{amount}"
    try:
        cache_data = redis_client.get(hash(key))
        if cache_data:
            return json.loads(cache_data.decode())
    except ConnectionError as e:
        logger.warning("Redis is not working")
        logger.error(str(e))

    logger.info(f"REDIS: missed key {key}")

    store = Store.objects.filter(id=store_id).first()
    promotion = Promotion.objects.filter(
        store=store,
        approved=True,
        category_id=category_id,
        min_price__lte=amount,
        max_price__gte=amount).order_by("-id").first()
    if not (promotion and store):
        try:
            redis_client.set(hash(key),
                             json.dumps({}).encode(),
                             ex=timedelta(days=30))
        except ConnectionError as e:
            logger.error(str(e))
        return {}

    data = PromotionSerializer(promotion).data
    try:
        redis_client.set(hash(key),
                         json.dumps(data).encode(),
                         ex=timedelta(days=30))
    except ConnectionError as e:
        logger.error(str(e))
    return data


def invalidate_promotion_cache(store_id, category_id):
    keys = f"promotions_{store_id}_{category_id}*"
    try:
        res = redis_client.delete(*keys)
        logger.info(f"REDIS: Deleted {res} keys")
    except ConnectionError as e:
        logger.error(str(e))
