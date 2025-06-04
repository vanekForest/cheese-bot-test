from schemas.enum_models import PaymentOperator
from services.payment.lava_payment import LavaPayment
from services.payment.stripe_payment import StripePayment
from services.payment.t_bank_payment import TBankPayment

PAYMENTS_OPERATORS = [LavaPayment(), StripePayment(), TBankPayment()]


async def generate_payment_url(
    amount: float, operator: PaymentOperator, label: str
) -> str:
    """
    Генерирует ссылку для оплаты.
    :param amount: Сумма платежа.
    :param operator: Оператор платежа (например, "LAVA", "RF_CARD", "STRIPE").
    :param label: Метка платежа.
    :return: Ссылка для оплаты.
    """
    for payment in PAYMENTS_OPERATORS:
        if payment.operator == operator:
            return await payment.generate_payment_link(amount=amount, label=label)
    raise ValueError(f"Unsupported payment operator: {operator}")
