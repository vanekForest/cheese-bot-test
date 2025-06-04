from enum import Enum


class StartAction(Enum):
    FURTHER_EXAMPLES = "further_examples"
    DESCRIPTION_PRODUCT = "description_product"


class PaymentAction(Enum):
    PRICE = "price"


class PaymentOperator(Enum):
    RF_CARD = "rf_card"
    STRIPE = "stripe"
    LAVA = "lava"


class PaymentStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class PhotoSection(str, Enum):
    START_IMAGE = "start_image"
    PRICE = "price"
    FARTHER_EXAMPLES = "further_examples"
    DESCRIPTION_PRODUCT = "description_product"
    BEST_POST = "best_post"


class MailType(Enum):
    NOT_SUBSCRIBE = "not_subscribe"
    NOT_SUCCESS_PAYMENT = "not_success_payment"
    MAIL_POST = "mail_post"
