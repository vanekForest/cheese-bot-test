from models.enum_models import PaymentOperator
from models.payment.base_payment import BasePayment


class LavaPayment(BasePayment):
    def __init__(self):
        super().__init__(operator=PaymentOperator.LAVA)

    async def generate_payment_link(self, label: str, amount: float) -> str:
        """
        Генерирует ссылку для оплаты через Lava.
        :param label: метка платежа.
        :param amount: сумма платежа.
        :return: ссылка для оплаты.
        """
        #TODO Здесь должна быть логика генерации ссылки для Lava
        return f"https://lava.example.com/pay?amount={amount}&label={label}"
