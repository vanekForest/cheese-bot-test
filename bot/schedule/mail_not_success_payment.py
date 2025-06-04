from sqlalchemy.ext.asyncio import AsyncSession

from config import PRICES
from keyboards.payment import payment_menu_keyboard
from schedule.utils import mail_to_users_with_photo
from schemas.db_models import User
from schemas.db_models.db_session import session_db
from schemas.enum_models import PhotoSection, MailType
from utils.message import msg


@session_db
async def mailing_task_not_success_payments(session: AsyncSession):
    """
    Отправляет текстовое сообщение пользователям, которые не совершили успешные платежи.
    :param session: Сессия базы данных.
    """
    user_ids = await User.get_not_successful_or_no_payments_telegram_ids(
        session=session
    )

    await mail_to_users_with_photo(
        user_ids=user_ids,
        photo_section=PhotoSection.PRICE.value,
        caption=msg("schedule", "3"),
        keyboard=payment_menu_keyboard(prices=PRICES["sale_offer"]),
        session=session,
        mail_type=MailType.NOT_SUCCESS_PAYMENT,
    )
