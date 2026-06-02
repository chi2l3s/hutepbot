from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, Payment

async def get_or_create_user(session: AsyncSession, user_id: int, username: str, full_name: str) -> User:
    user = await session.get(User, user_id)
    if not user:
        user = User(id=user_id, username=username, full_name=full_name)
        session.add(user)
        await session.commit()
    return user

async def get_or_create_pending_payment(
    session: AsyncSession,
    user_id: int,
    amount: int,
    months: int,
    provider: str,
    external_id: str,
    telegram_payment_charge_id: str | None = None,
) -> Payment:
    result = await session.execute(
        select(Payment).where(
            Payment.provider == provider,
            Payment.external_id == external_id,
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing

    payment = Payment(
        user_id=user_id,
        amount=amount,
        months=months,
        provider=provider,
        external_id=external_id,
        status='pending',
        telegram_payment_charge_id=telegram_payment_charge_id,
        is_successful=False,
    )
    session.add(payment)
    await session.commit()
    return payment

async def mark_payment_successful(session: AsyncSession, payment: Payment) -> Payment:
    payment.status = 'successful'
    payment.is_successful = True
    await session.commit()
    return payment