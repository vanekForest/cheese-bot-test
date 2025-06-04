import datetime
from typing import Optional, Self, List

from sqlalchemy import Integer, BigInteger, String, select, DateTime, func, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, aliased

from schemas.db_models import Payment
from schemas.db_models.db_session import Base
from schemas.enum_models import PaymentStatus


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
    async def get_all_user_telegram_ids(cls, session: AsyncSession) -> list[int]:
        """
        Получение всех telegram id пользователей
        :param session: асинхронная сессия
        :return: список всех пользователей
        """
        query = select(cls.telegram_id).where(cls.is_active.is_(True))
        result = await session.execute(query)
        return list(result.scalars().all())

    @classmethod
    async def get_not_successful_or_no_payments_telegram_ids(
        cls, session: AsyncSession
    ) -> list[int]:
        """
        Получение уникальных telegram_id пользователей, у которых либо нет платежей,
        либо есть платежи, но ни один из них не имеет статус SUCCESS.
        :param session: асинхронная сессия
        :return: список уникальных telegram_id
        """
        payment_alias = aliased(Payment)

        subquery = (
            select(payment_alias.user_id)
            .where(payment_alias.status == PaymentStatus.SUCCESS)
            .subquery()
        )

        query = (
            select(cls.telegram_id)
            .outerjoin(payment_alias, payment_alias.user_id == cls.id)
            .where(~cls.id.in_(select(subquery.c.user_id)), cls.is_active.is_(True))
        )

        result = await session.execute(query)
        return list(set(result.scalars().all()))

    @classmethod
    async def update_user_activity(
        cls, telegram_id: int, is_active: bool, session: AsyncSession
    ) -> None:
        """
        Обновление активности пользователя по его Telegram ID.
        :param telegram_id: Telegram ID пользователя.
        :param is_active: Флаг активности пользователя.
        :param session: Асинхронная сессия.
        """
        query = select(cls).where(cls.telegram_id == telegram_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user:
            user.is_active = is_active
            session.add(user)
            await session.commit()
