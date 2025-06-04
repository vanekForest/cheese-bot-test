from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.callback_factory import (
    StartActionCallbackFactory,
    StartAction,
    PaymentActionCallbackFactory,
    PaymentAction,
)
from utils.message import btn


def start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=btn("start", "1"),
        callback_data=StartActionCallbackFactory(action=StartAction.FURTHER_EXAMPLES),
    )
    builder.button(
        text=btn("start", "2"),
        callback_data=PaymentActionCallbackFactory(action=PaymentAction.PRICE),
    )
    builder.adjust(2)
    return builder.as_markup()


def further_examples_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=btn("start", "3"),
        callback_data=StartActionCallbackFactory(
            action=StartAction.DESCRIPTION_PRODUCT
        ),
    )
    builder.adjust(1)
    return builder.as_markup()


def description_product_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=btn("start", "4"),
        callback_data=PaymentActionCallbackFactory(action=PaymentAction.PRICE),
    )
    builder.adjust(1)
    return builder.as_markup()
