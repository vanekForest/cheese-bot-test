from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, Double, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLAlchemyEnum

from db_models.db_session import Base
from models.enum_models import PaymentStatus, PaymentOperator


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
                                         nullable=False)
    amount: Mapped[float] = mapped_column(Double, nullable=False)
    operator: Mapped[PaymentOperator] = mapped_column(SQLAlchemyEnum(PaymentOperator), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(SQLAlchemyEnum(PaymentStatus), nullable=False,
                                                  default=PaymentStatus.PENDING)
    label: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)

    user: Mapped["User"] = relationship("User", back_populates="payments", lazy="selectin")
