from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Numeric, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(64))
    full_name: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    payments: Mapped[list['Payment']] = relationship(back_populates='user')

class Payment(Base):
    __tablename__ = 'payments'
    __table_args__ = (
        UniqueConstraint('provider', 'external_id', name='uq_payments_provider_external_id'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'))
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    months: Mapped[int]
    provider: Mapped[str]
    external_id: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(16), default='pending')
    telegram_payment_charge_id: Mapped[str | None] = mapped_column(String(256), nullable=True, default=None)
    is_successful: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped['User'] = relationship(back_populates='payments')