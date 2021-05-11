import os
from django.core.exceptions import ValidationError


MAX_FILE_SIZE = 1024000
ALLOWED_EXTENSIONS = ['.jpg', '.png']
MAX_REVIEW_RATE = 5
MIN_REVIEW_RATE = 0
MIN_CARD_NUMBER = 16
MIN_CARD_CVV = 3


def validate_size(value):
    if value.size >= MAX_FILE_SIZE:
        raise ValidationError(f'max file size is: {MAX_FILE_SIZE}')


def validate_extension(value):
    split_ext = os.path.splitext(value.name)

    if len(split_ext) > 1:
        ext = split_ext[1]
        if ext.lower() not in ALLOWED_EXTENSIONS:
            raise ValidationError(f'not allowed file, valid extensions: {ALLOWED_EXTENSIONS}')


def validate_review(value):
    if value > MAX_REVIEW_RATE or value <= MIN_REVIEW_RATE:
        raise ValidationError(f'review rate range is between 1 and 5')


def validate_card_number(value):
    if value.size < MIN_CARD_NUMBER:
        raise ValidationError(f'card number size must be 16 digits')


def validate_card_cvv(value):
    if value.size < MIN_CARD_CVV:
        raise ValidationError(f'card cvv size must be 3 digits')


def validate_phone_number(value):
    if value[0] != '+':
        raise ValidationError(f'phone number is incorrect')
