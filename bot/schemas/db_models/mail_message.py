from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, DateTime, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import Enum as SQLAlchemyEnum

from schemas.db_models.db_session import Base
from schemas.enum_models import MailType


class MailMessage(Base):
    __tablename__ = "mail_messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    mail_type: Mapped[MailType] = mapped_column(SQLAlchemyEnum(MailType))
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    @classmethod
    async def get_count_message_by_mail_type_and_user_id(
        cls, mail_type: MailType, user_id: int, session: AsyncSession
    ) -> int:
        """
        Получить количество сообщений по типу и телеграм ID
        :param session: асинхронная сессия
        :param mail_type: тип сообщения
        :param user_id: ID пользователя
        :return количество сообщений
        """

        query = select(func.count(cls.id)).where(
            cls.mail_type == mail_type, cls.user_id == user_id
        )
        result = await session.execute(query)
        return int(result.scalar())
