from faststream.rabbit import RabbitBroker

from config import QUEUE_PUBLISHER_RABBIT, RABBIT_URL


class RabbitPublishService:
    def __init__(self):
        self.broker = RabbitBroker(RABBIT_URL)

    async def __aenter__(self):
        await self.broker.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.broker.close()

    async def send_result(self, message: dict, queue: str):
        await self.broker.publish(
            message,
            queue=queue
        )

    async def publish_data(self, message: dict):
        await self.send_result(message=message, queue=QUEUE_PUBLISHER_RABBIT)
