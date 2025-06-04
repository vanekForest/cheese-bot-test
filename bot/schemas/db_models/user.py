import datetime
from typing import Optional, Self, List

from sqlalchemy import (
    Integer,
    BigInteger,
    String,
    select,
    DateTime,
    func,
    Boolean,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, aliased

from config import MAX_COUNT_MAIL_MESSAGES, __log__
from schemas.db_models import Payment, MailMessage
from schemas.db_models.db_session import Base
from schemas.enum_models import PaymentStatus, MailType


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_accession: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    payments: Mapped[List["Payment"]] = relationship(
        "Payment", back_populates="user", lazy="selectin"
    )
    subscribe: Mapped["User"] = relationship(
        "Subscribe", back_populates="user", uselist=False, lazy="selectin"
    )

    @classmethod
    async def get_user_by_telegram_id(
        cls, telegram_id: int, session: AsyncSession
    ) -> Self | None:
        """
        Получение пользователя по его Telegram ID
        :param telegram_id: Telegram ID пользователя
        :param session: асинхронная сессия
        :return: объект пользователя или None, если пользователь не найден
        """
        query = select(cls).where(cls.telegram_id == telegram_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_not_successful_or_no_payments_telegram_ids(
        cls, session: AsyncSession
    ) -> list[int]:
        """
        Получение уникальных telegram_id пользователей, у которых либо нет платежей,
        либо есть платежи, но ни один из них не имеет статус SUCCESS, и при этом
        количество отправленных сообщений типа NOT_SUCCESS_PAYMENT < MAX_COUNT_MAIL_MESSAGES.
        """
        payment_alias = aliased(Payment)
        mail_alias = aliased(MailMessage)

        # Подзапрос: пользователи с успешными платежами
        successful_payment_subq = (
            select(payment_alias.user_id)
            .where(payment_alias.status == PaymentStatus.SUCCESS)
            .subquery()
        )

        # Основной запрос
        query = (
            select(cls.telegram_id)
            .outerjoin(
                mail_alias,
                (cls.id == mail_alias.user_id)
                & (mail_alias.mail_type == MailType.NOT_SUCCESS_PAYMENT),
            )
            .where(
                ~cls.id.in_(select(successful_payment_subq.c.user_id)),
                cls.is_active.is_(True),
            )
            .group_by(cls.id)
            .having(func.count(mail_alias.id) < MAX_COUNT_MAIL_MESSAGES)
        )

        result = await session.execute(query)
        return list(result.scalars().all())

    @classmethod
    async def update_user_activity(
        cls, telegram_id: int, is_active: bool, session: AsyncSession
    ) -> None:
        """
        Обновление активности пользователя по Telegram ID с использованием update().
        :param telegram_id: Telegram ID пользователя.
        :param is_active: Флаг активности пользователя.
        :param session: Асинхронная сессия.
        """
        query = (
            update(cls)
            .where(cls.telegram_id == telegram_id)
            .values(is_active=is_active)
        )
        await session.execute(query)
        await session.commit()

    @classmethod
    async def get_all_user_telegram_ids_by_mail_message_type(
        cls, mail_type: MailType, session: AsyncSession
    ) -> list[int]:
        """
        Получение всех ID пользователей, которым нужно отправить сообщение определённого типа.
        :param mail_type: тип рассылки
        :return: список ID пользователей
        """
        query = (
            select(User.telegram_id)
            .outerjoin(
                MailMessage,
                (User.id == MailMessage.user_id) & (MailMessage.mail_type == mail_type),
            )
            .group_by(User.id)
            .having(func.count(MailMessage.id) < MAX_COUNT_MAIL_MESSAGES)
        )
        __log__.info(query)
        result = await session.execute(query)
        return list(result.scalars().all())
