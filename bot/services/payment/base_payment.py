from abc import ABC, abstractmethod

from schemas.enum_models import PaymentOperator


class BasePayment(ABC):
    def __init__(self, operator: PaymentOperator):
        self.operator = operator

    def check(self, operator: PaymentOperator) -> bool:
        return self.operator == operator

    @abstractmethod
    async def generate_payment_link(self, **kwargs) -> str:
        """
        Генерирует ссылку для оплаты.
        :param kwargs: аргументы, которые могут понадобиться для генерации ссылки.
        :return: ссылка для оплаты.д
        """
        pass
