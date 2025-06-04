from aiogram.filters.callback_data import CallbackData

from schemas.enum_models import StartAction, PaymentAction, PaymentOperator


class StartActionCallbackFactory(CallbackData, prefix="start_action"):
    action: StartAction


class PaymentActionCallbackFactory(CallbackData, prefix="payment_action"):
    action: PaymentAction


class PaymentOperatorCallbackFactory(CallbackData, prefix="payment_operator_action"):
    operator: PaymentOperator
    amount: float
