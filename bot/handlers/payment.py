import datetime

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.db_models import User
from schemas.db_models.db_session import session_db
from schemas.db_models.payments import Payment
from keyboards.payment import payment_url_keyboard
from utils.callback_factory import PaymentOperatorCallbackFactory
from utils.generate import generate_payment_url
from utils.message import msg

router = Router()


@router.callback_query(PaymentOperatorCallbackFactory.filter())
@session_db
async def payment(
    callback: CallbackQuery, callback_data: CallbackData, session: AsyncSession
):
    text = msg("payment", callback_data.operator.value)
    label = str(callback.from_user.id) + "_" + str(datetime.datetime.now())
    await callback.message.answer(
        text=text,
        reply_markup=payment_url_keyboard(
            payment_url=await generate_payment_url(
                operator=callback_data.operator,
                amount=callback_data.amount,
                label=label,
            )
        ),
    )
    user = await User.get_user_by_telegram_id(
        telegram_id=callback.from_user.id, session=session
    )
    payment = Payment(
        user_id=user.id,
        amount=callback_data.amount,
        operator=callback_data.operator,
        label=label,
    )
    await payment.save(session=session)
