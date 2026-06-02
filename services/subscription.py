from datetime import datetime, timezone, timedelta
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from db.repository import (
    get_or_create_pending_payment,
    mark_payment_successful
)
from services.vpn import vpn_service
from constants import PLANS


def _new_expiry(current: datetime | int  | None, months: int) -> datetime:
    now = datetime.now(timezone.utc)

    if isinstance(current, (int, float)):
        current = datetime.fromtimestamp(current / 1000, tz=timezone.utc)

    base = current if current and current > now else now
    return base + timedelta(days=30 * months)


async def activate_subscription(
    session: AsyncSession,
    user_id: int,
    plan_key: str,
    amount: int,
    provider: str,
    external_id: str,
    telegram_payment_charge_id: str | None = None,
) -> bool:
    plan = PLANS[plan_key]
    months = plan['months']

    payment = await get_or_create_pending_payment(
        session=session,
        user_id=user_id,
        amount=amount,
        months=months,
        provider=provider,
        external_id=external_id,
        telegram_payment_charge_id=telegram_payment_charge_id,
    )

    if payment.status == 'successful':
        logger.info(f'Платёж {provider}:{external_id} уже обработан')
        return True

    subscription = await vpn_service.get_client(user_id)
    new_expires_at = _new_expiry(
    subscription.expiry_time if subscription else None,
        months
    )

    expiry_ms = int(new_expires_at.timestamp() * 1000)

    if subscription:
        if not await vpn_service.update_expiry(user_id, expiry_ms=expiry_ms):
            logger.error(f'Не удалось продлить VPN клиента {user_id} в панели')
            return False
        logger.success(f'VPN клиент продлён для {user_id} до {new_expires_at}')
    else:
        client = await vpn_service.get_client(user_id)
        if client:
            if not await vpn_service.update_expiry(user_id, expiry_ms=expiry_ms):
                logger.error(f'Не удалось продлить VPN клиента {user_id} в панели')
                return False
            await vpn_service.create_client(
                user_id,
                expiry_ms=expiry_ms
            )
            logger.success(f'Существующий VPN клиент {user_id} привязан к БД, продлён до {new_expires_at}')
        else:
            created = await vpn_service.create_client(user_id, expiry_ms=expiry_ms)
            if not created or not created.get('success'):
                logger.error(f'Не удалось создать VPN клиента {user_id}')
                return False
            fresh = await vpn_service.get_client(user_id)
            if not fresh:
                logger.error(f'VPN клиент {user_id} создан, но не найден повторным запросом')
                return False
            await vpn_service.create_client(
                user_id,
                expiry_ms=expiry_ms
            )
            logger.success(f'VPN клиент создан для {user_id} до {new_expires_at}')

    await mark_payment_successful(session, payment)
    logger.success(f'Подписка активирована: {user_id} — {plan["label"]}')
    return True
