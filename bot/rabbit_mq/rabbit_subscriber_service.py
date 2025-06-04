from faststream import FastStream

from config import broker, QUEUE_SUBSCRIBER_RABBIT
from db_models.db_session import global_init

app = FastStream(broker)


@app.on_startup
async def on_startup():
    await global_init()


@broker.subscriber(QUEUE_SUBSCRIBER_RABBIT)
async def subscribe_data_service(message: dict):
    await subscribe_data(message)


async def subscribe_data(message: dict):
    pass
