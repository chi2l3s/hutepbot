from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.purchase import plans_keyboard, payment_methods_kb
from services.crypto import create_invoice, check_payment
from services.subscription import activate_subscription
from services.platega import create_payment_url
from states import PaymentState
from constants import PLANS

router = Router(name='purchase')


@router.callback_query(F.data == 'purchase')
async def show_plans(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(PaymentState.choosing_plan)
    await callback.message.edit_text(
        f'Выберите план подписки:',
        reply_markup=plans_keyboard()
    )


@router.callback_query(PaymentState.choosing_plan, F.data.in_(PLANS.keys()))
async def choose_method(callback: CallbackQuery, state: FSMContext):
    plan = PLANS[callback.data]
    await state.update_data(plan_key=callback.data)
    await state.set_state(PaymentState.choosing_method)

    await callback.answer()
    await callback.message.edit_text(
        f"📦 Тариф: <b>{plan['label']}</b>\n"
        f"💰 Цена: <b>{plan['price']} ₽</b>\n\n"
        "Выбери способ оплаты:",
        reply_markup=payment_methods_kb()
    )


@router.callback_query(PaymentState.choosing_method, F.data == 'pay_stars')
async def pay_stars(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    plan = PLANS[data['plan_key']]

    await state.clear()
    await callback.answer()
    await callback.message.answer_invoice(
        title=f'VPN — {plan['label']}',
        description=f'Подписка на {plan['label']}',
        payload=f'{data['plan_key']}:{callback.from_user.id}',
        currency='XTR',
        prices=[LabeledPrice(label=plan['label'], amount=plan['stars'])]
    )


@router.callback_query(PaymentState.choosing_method, F.data == 'pay_card')
async def pay_card(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    plan = PLANS[data['plan_key']]

    transaction_url = await create_payment_url(plan['price'], plan_key=plan['plan_key'], user_id=callback.from_user.id)
    
    kb = InlineKeyboardBuilder()
    kb.button(text=f"💳 Оплатить {plan['price']} ₽", url=transaction_url)
    
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        f"💳 Оплата картой\n\n"
        f"Тариф: <b>{plan['label']}</b>\n"
        f"Сумма: <b>{plan['price']} ₽</b>",
        reply_markup=kb.as_markup()
    )


@router.callback_query(PaymentState.choosing_method, F.data == 'pay_crypto')
async def pay_crypto(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    plan = PLANS[data['plan_key']]

    amount = plan['price']

    invoice_url = await create_invoice(
        amount=amount,
        plan_key=data['plan_key'],
        user_id=callback.from_user.id
    )

    kb = InlineKeyboardBuilder()
    kb.button(text=f"💰 Оплатить {amount} RUB", url=invoice_url)
    kb.button(text="✅ Я оплатил",
              callback_data=f"check_crypto:{data['plan_key']}")
    kb.adjust(1)

    await callback.message.edit_text(
        f"💰 Оплата криптой\n\n"
        f"Тариф: <b>{plan['label']}</b>\n"
        f"Сумма: <b>{amount} RUB</b>\n\n"
        f"Нажми кнопку ниже для оплаты:",
        reply_markup=kb.as_markup()
    )


@router.callback_query(F.data == 'back_plans')
async def back_main_handler(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        f'Выберите план подписки:',
        reply_markup=plans_keyboard()
    )


@router.message(F.successful_payment)
async def successful_payment(message: Message, session: AsyncSession):
    payment = message.successful_payment
    plan_key, user_id = payment.invoice_payload.split(':')
    plan = PLANS[plan_key]

    ok = await activate_subscription(
        session=session,
        user_id=int(user_id),
        plan_key=plan_key,
        amount=payment.total_amount,
        provider='stars',
        external_id=payment.telegram_payment_charge_id,
        telegram_payment_charge_id=payment.telegram_payment_charge_id,
    )

    if ok:
        await message.answer(
            f'✅ Оплата прошла!\n\n'
            f'🔒 Подписка на <b>{plan["label"]}</b> активирована.'
        )
    else:
        await message.answer(
            '⚠️ Оплата получена, но не удалось выдать VPN. Напиши в поддержку — мы всё починим.'
        )


@router.callback_query(F.data.startswith("check_crypto:"))
async def check_crypto_payment(callback: CallbackQuery, session: AsyncSession):
    plan_key = callback.data.split(':')[1]

    invoice_id = await check_payment(plan_key=plan_key, user_id=callback.from_user.id)

    if not invoice_id:
        await callback.answer("❌ Оплата не найдена, попробуй позже", show_alert=True)
        return

    ok = await activate_subscription(
        session=session,
        user_id=callback.from_user.id,
        plan_key=plan_key,
        amount=PLANS[plan_key]['stars'],
        provider='cryptobot',
        external_id=invoice_id,
    )

    if ok:
        await callback.message.edit_text("✅ Подписка активирована!")
    else:
        await callback.answer("⚠️ Не удалось выдать VPN. Напиши в поддержку.", show_alert=True)
