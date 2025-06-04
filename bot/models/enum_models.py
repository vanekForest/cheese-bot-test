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