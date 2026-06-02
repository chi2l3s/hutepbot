from aiogram.fsm.state import State, StatesGroup

class PaymentState(StatesGroup):
    choosing_plan = State()
    choosing_method = State()