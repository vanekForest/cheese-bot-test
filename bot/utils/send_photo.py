from aiogram.types import Message, InlineKeyboardMarkup, FSInputFile

from config import IMAGES, bot
from utils.message import img


async def send_photo(
    message: Message,
    photo_section: str,
    caption: str = None,
    keyboard: InlineKeyboardMarkup | None = None,
) -> None:
    """
    Отправляет фотографию вместе с подписью и клавиатурой (опционально).
    Если telegram_id есть у фото и с ним все в порядке, то отправляет его по file_id,
    если нет, то отправляет по пути к файлу.
    :param message: Сообщение, в которое будет отправлена фотография.
    :param photo_section: Секция, в которой хранится фото в json.
    :param caption: Подпись к фотографии.
    :param keyboard: Клавиатура, которая будет прикреплена к сообщению.
    """
    photo = img(photo_section)
    try:
        await message.answer_photo(
            photo=photo['file_id'], caption=caption, reply_markup=keyboard
        )
    except Exception:
        image = await message.answer_photo(
            photo=FSInputFile(photo["path"]), caption=caption, reply_markup=keyboard
        )
        file_id = image.photo[-1].file_id
        IMAGES[photo_section]['file_id'] = file_id


async def send_photo_by_user_id(
    user_id: int,
    photo_section: str,
    caption: str = None,
    keyboard: InlineKeyboardMarkup | None = None,
) -> None:
    """
    Отправляет фотографию пользователю по его Telegram ID.
    :param user_id: ID пользователя в Telegram.
    :param photo_section: Секция, в которой хранится фото в json.
    :param caption: Подпись к фотографии.
    :param keyboard: Клавиатура, которая будет прикреплена к сообщению.
    """
    photo = img(photo_section)
    try:
        await bot.send_photo(
            chat_id=user_id,
            photo=photo['file_id'],
            caption=caption,
            reply_markup=keyboard,
        )
    except Exception:
        image = await bot.send_photo(
            chat_id=user_id,
            photo=FSInputFile(photo["path"]),
            caption=caption,
            reply_markup=keyboard,
        )
        file_id = image.photo[-1].file_id
        IMAGES[photo_section]['file_id'] = file_id
