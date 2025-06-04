from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.callback_factory import PaymentOperatorCallbackFactory
from schemas.enum_models import PaymentOperator
from utils.message import btn, url


def payment_menu_keyboard(prices: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=btn("payment", "1"),
        callback_data=PaymentOperatorCallbackFactory(
            operator=PaymentOperator.RF_CARD, amount=prices["rf_card"]["price"]
        ),
    )
    builder.button(
        text=btn("payment", "2"),
        callback_data=PaymentOperatorCallbackFactory(
            operator=PaymentOperator.STRIPE, amount=prices["stripe"]["price"]
        ),
    )
    builder.button(
        text=btn("payment", "3"),
        callback_data=PaymentOperatorCallbackFactory(
            operator=PaymentOperator.LAVA, amount=prices["lava"]["price"]
        ),
    )
    builder.button(text=btn("payment", "4"), url=url("1"))
    builder.adjust(2)
    return builder.as_markup()


def payment_url_keyboard(payment_url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=btn("payment", "5"), url=payment_url)
    builder.adjust(1)
    return builder.as_markup()
