from schemas.enum_models import PaymentOperator
from services.payment.base_payment import BasePayment


class TBankPayment(BasePayment):
    def __init__(self):
        super().__init__(operator=PaymentOperator.RF_CARD)

    async def generate_payment_link(self, amount: float, label: str) -> str:
        """
        Генерирует ссылку для оплаты через TBank.
        :param amount: сумма платежа.
        :param label: метка платежа.
        :return: ссылка для оплаты.
        """
        # TODO Здесь должна быть логика генерации ссылки для TBank
        return f"https://tbank.example.com/pay?amount={amount}&label={label}"
