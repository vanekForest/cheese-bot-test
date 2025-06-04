from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from config import PRICES
from schemas.db_models import User
from schemas.db_models.db_session import session_db
from schemas.db_models import Subscribe
from keyboards.payment import payment_menu_keyboard
from keyboards.start import (
    start_keyboard,
    further_examples_keyboard,
    description_product_keyboard,
)
from schemas.enum_models import PhotoSection
from utils.callback_factory import (
    StartActionCallbackFactory,
    StartAction,
    PaymentActionCallbackFactory,
    PaymentAction,
)
from utils.message import msg
from utils.send_photo import send_photo

router = Router()


@router.message(Command("start"))
@session_db
async def start(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    user = await User.get_user_by_telegram_id(message.from_user.id, session=session)
    if not user:
        user = User(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )
        await user.save(session=session)
        subscribe = Subscribe(user_id=user.id)
        await subscribe.save(session=session)
    await send_photo(
        message=message,
        photo_section=PhotoSection.START_IMAGE.value,
        caption=msg("start", "1"),
        keyboard=start_keyboard(),
    )


@router.callback_query(
    StartActionCallbackFactory.filter(F.action == StartAction.FURTHER_EXAMPLES)
)
async def further_examples(callback: CallbackQuery):
    await callback.answer()
    await send_photo(
        message=callback.message,
        photo_section=PhotoSection.FARTHER_EXAMPLES.value,
        caption=msg("start", "2"),
        keyboard=further_examples_keyboard(),
    )


@router.callback_query(
    StartActionCallbackFactory.filter(F.action == StartAction.DESCRIPTION_PRODUCT)
)
async def description_product(callback: CallbackQuery):
    await callback.answer()
    await send_photo(
        message=callback.message,
        photo_section=PhotoSection.DESCRIPTION_PRODUCT.value,
        caption=msg("start", "3"),
        keyboard=description_product_keyboard(),
    )


@router.callback_query(
    PaymentActionCallbackFactory.filter(F.action == PaymentAction.PRICE)
)
async def get_price(callback: CallbackQuery):
    await callback.answer()
    await send_photo(
        message=callback.message,
        photo_section=PhotoSection.PRICE.value,
        caption=msg("start", "4"),
        keyboard=payment_menu_keyboard(prices=PRICES["regular_offer"]),
    )
