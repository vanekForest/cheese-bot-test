from models.enum_models import PaymentOperator
from models.payment.base_payment import BasePayment


class StripePayment(BasePayment):
    def __init__(self):
        super().__init__(operator=PaymentOperator.STRIPE)

    async def generate_payment_link(self, amount: float, label: str) -> str:
        """
        Генерирует ссылку для оплаты через Stripe.
        :param amount: сумма платежа.
        :return: ссылка для оплаты.
        """
        # TODO Здесь должна быть логика генерации ссылки для Stripe
        return f"https://stripe.example.com/pay?amount={amount}&label={label}"
