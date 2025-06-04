import asyncio

from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramRetryAfter, TelegramAPIError, TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from config import bot, CHANNEL_ID, PRICES
from db_models import User
from db_models.db_session import session_db
from keyboards.payment import payment_menu_keyboard
from utils.message import msg
from utils.send_photo import send_photo_by_user_id


@session_db
async def mailing_task_not_subscribe(session: AsyncSession):
    """
    Отправляет текстовое сообщение пользователям, которые не подписаны на канал.
    :param session: Сессия базы данных.
    """
    user_ids = await User.get_all_user_telegram_ids(session=session)

    await _mail_to_users(user_ids=await _get_unsubscribed_users(user_ids=user_ids, channel_id=CHANNEL_ID),
                         text=msg("schedule", "1"))


async def _mail_to_users(user_ids: list[int], text: str):
    """
    Отправляет текстовое сообщение пользователям по их Telegram ID.

    :param user_ids: Список ID пользователей в Telegram.
    :param text: Текст сообщения для отправки.
    """

    for user in user_ids:
        try:
            await bot.send_message(chat_id=user, text=text)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await bot.send_message(chat_id=user, text=text)
        except TelegramAPIError as e:
            pass


async def _get_unsubscribed_users(user_ids: list[int], channel_id: str) -> list[int]:
    unsubscribed_users = []

    for user_id in user_ids:
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
                unsubscribed_users.append(user_id)
        except TelegramBadRequest:
            unsubscribed_users.append(user_id)
        except Exception as e:
            print(f"Ошибка при проверке {user_id}: {e}")

    return unsubscribed_users


@session_db
async def mailing_task_not_success_payments(session: AsyncSession):
    """
    Отправляет текстовое сообщение пользователям, которые не совершили успешные платежи.
    :param session: Сессия базы данных.
    """
    user_ids = await User.get_not_successful_or_no_payments_telegram_ids(session=session)

    await _mail_to_users_with_photo(user_ids=user_ids, photo_section="price", caption=msg("schedule", "3"),
                                    keyboard=payment_menu_keyboard(prices=PRICES["sale_offer"]))


async def _mail_to_users_with_photo(user_ids: list[int], caption: str, photo_section: str,
                                    keyboard: InlineKeyboardMarkup | None = None):
    """
    Отправляет текстовое сообщение пользователям по их Telegram ID.

    :param user_ids: Список ID пользователей в Telegram.
    :param text: Текст сообщения для отправки.
    """

    for user in user_ids:
        try:
            await send_photo_by_user_id(user_id=user, caption=caption, photo_section=photo_section, keyboard=keyboard)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await bot.send_message(user_id=user, text=caption)
        except TelegramAPIError as e:
            pass

@session_db
async def mailing_task_post(session: AsyncSession):
    """
    Отправляет текстовое сообщение с постом всем пользователям
    :param session:
    :return:
    """
    user_ids = await User.get_all_user_telegram_ids(session=session)
    await _mail_to_users_with_photo(user_ids=user_ids, photo_section="best_post", caption=msg("schedule", "2"))
