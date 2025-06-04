import asyncio
import logging
from aiogram import Dispatcher, BaseMiddleware
from aiogram.fsm.state import StatesGroup, State

from config import (
    bot,
    POST_SCHEDULED_TASK_INTERVAL,
    SUBSCRIBE_SCHEDULED_TASK_INTERVAL,
    SALE_OFFER_SCHEDULED_TASK_INTERVAL,
)
from config import storage
from schedule.mail_not_subscribe import mailing_task_not_subscribe
from schedule.mail_not_success_payment import mailing_task_not_success_payments
from schedule.mail_post import mailing_task_post
from schemas.db_models.db_session import global_init
from handlers import start, payment
from schedule.schedule import ScheduledTask


class MailMessage(StatesGroup):
    message = State()


def bind_middleware_everywhere(dp: Dispatcher, mw: BaseMiddleware):
    dp.message.middleware(mw)
    dp.callback_query.middleware(mw)
    dp.edited_message.middleware(mw)
    dp.channel_post.middleware(mw)
    dp.edited_channel_post.middleware(mw)
    dp.inline_query.middleware(mw)
    dp.chosen_inline_result.middleware(mw)
    dp.shipping_query.middleware(mw)
    dp.pre_checkout_query.middleware(mw)
    dp.poll.middleware(mw)
    dp.poll_answer.middleware(mw)


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота

# Диспетчер
dp = Dispatcher(storage=storage)

dp.include_routers(start.router, payment.router)


async def main():
    await global_init()

    # Список задач с интервалами
    scheduled_tasks = [
        (mailing_task_not_subscribe, SUBSCRIBE_SCHEDULED_TASK_INTERVAL),
        (mailing_task_not_success_payments, SALE_OFFER_SCHEDULED_TASK_INTERVAL),
        (mailing_task_post, POST_SCHEDULED_TASK_INTERVAL),
    ]

    scheduler = ScheduledTask(scheduled_tasks)

    await asyncio.gather(
        scheduler.start(),
        dp.start_polling(bot),
    )


if __name__ == "__main__":
    asyncio.run(main())
