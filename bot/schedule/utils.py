import asyncio

from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import (
    TelegramRetryAfter,
    TelegramBadRequest,
    TelegramForbiddenError,
)
from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from config import bot
from schemas.db_models import User
from schemas.db_models.mail_message import MailMessage
from schemas.enum_models import MailType
from utils.send_photo import send_photo_by_user_id


async def mail_to_users(
    user_ids: list[int], text: str, mail_type: MailType, session: AsyncSession
):
    """
    Отправляет текстовое сообщение пользователям по их Telegram ID.

    :param user_ids: Список ID пользователей в Telegram.
    :param text: Текст сообщения для отправки.
    """

    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text=text)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await bot.send_message(chat_id=user_id, text=text)
        except TelegramForbiddenError:
            await User.update_user_activity(
                telegram_id=user_id, is_active=False, session=session
            )
        await MailMessage(user_id=user_id, mail_type=mail_type).save(session=session)


async def get_unsubscribed_users(user_ids: list[int], channel_id: str) -> list[int]:
    unsubscribed_users = []

    for user_id in user_ids:
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status not in [
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.CREATOR,
                ChatMemberStatus.ADMINISTRATOR,
            ]:
                unsubscribed_users.append(user_id)
        except TelegramBadRequest:
            unsubscribed_users.append(user_id)

    return unsubscribed_users


async def mail_to_users_with_photo(
    user_ids: list[int],
    caption: str,
    photo_section: str,
    mail_type: MailType,
    session: AsyncSession,
    keyboard: InlineKeyboardMarkup | None = None,
):
    """
    Отправляет текстовое сообщение пользователям по их Telegram ID.

    :param user_ids: Список ID пользователей в Telegram.
    :param text: Текст сообщения для отправки.
    :param photo_section: Раздел фото для отправки.
    :param mail_type: Тип рассылки.
    :param session: Сессия базы данных.
    """

    for user_id in user_ids:
        try:
            await send_photo_by_user_id(
                user_id=user_id,
                caption=caption,
                photo_section=photo_section,
                keyboard=keyboard,
            )
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await send_photo_by_user_id(
                user_id=user_id,
                caption=caption,
                photo_section=photo_section,
                keyboard=keyboard,
            )
        except TelegramForbiddenError:
            await User.update_user_activity(
                telegram_id=user_id, is_active=False, session=session
            )
        await MailMessage(user_id=user_id, mail_type=mail_type).save(session=session)
