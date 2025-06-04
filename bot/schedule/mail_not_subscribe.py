from sqlalchemy.ext.asyncio import AsyncSession

from config import CHANNEL_ID
from schedule.utils import mail_to_users, get_unsubscribed_users
from schemas.db_models import User
from schemas.db_models.db_session import session_db
from schemas.enum_models import MailType
from utils.message import msg


@session_db
async def mailing_task_not_subscribe(session: AsyncSession):
    """
    Отправляет текстовое сообщение пользователям, которые не подписаны на канал.
    :param session: Сессия базы данных.
    """
    user_ids = await User.get_all_user_telegram_ids(session=session)

    await mail_to_users(
        user_ids=await get_unsubscribed_users(user_ids=user_ids, channel_id=CHANNEL_ID),
        text=msg("schedule", "1"),
        session=session,
        mail_type=MailType.NOT_SUBSCRIBE,
    )
