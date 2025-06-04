from sqlalchemy.ext.asyncio import AsyncSession

from schedule.utils import mail_to_users_with_photo
from schemas.db_models import User
from schemas.db_models.db_session import session_db
from schemas.enum_models import PhotoSection, MailType
from utils.message import msg
from config import __log__


@session_db
async def mailing_task_post(session: AsyncSession):
    """
    Отправляет текстовое сообщение с постом всем пользователям
    :param session:
    :return:
    """
    user_ids = await User.get_all_user_telegram_ids_by_mail_message_type(
        mail_type=MailType.MAIL_POST, session=session
    )
    __log__.info(f"Mailing task post started for {len(user_ids)} users.")
    await mail_to_users_with_photo(
        user_ids=user_ids,
        photo_section=PhotoSection.BEST_POST.value,
        caption=msg("schedule", "2"),
        mail_type=MailType.MAIL_POST,
        session=session,
    )
