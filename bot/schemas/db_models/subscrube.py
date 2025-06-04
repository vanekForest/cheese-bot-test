from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from schemas.db_models.db_session import Base


class Subscribe(Base):
    __tablename__ = "subscribes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    remaining_count_images: Mapped[int] = mapped_column(BigInteger, default=0)

    user: Mapped["User"] = relationship(
        "User", back_populates="subscribe", lazy="selectin"
    )
