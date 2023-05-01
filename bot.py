import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

from name_filter import NameFilter
from serial_filter import SerialFilter

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s]%(asctime)s - %(name)s.%(funcName)s - %(message)s"
)

bot = Bot(token='')
dp = Dispatcher(storage=MemoryStorage())

class StGroup(StatesGroup):
    entrypoint = State()
    name = State()


@dp.message(Command('Start'))
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.username}")

@dp.message(SerialFilter())
async def serials_message(
    message: types.Message,
    correct_serials: dict,
    incorrect_serials: dict
):
    await message.answer(
        text=f"Серийные номера: {correct_serials}\n"
        f"Неправильные серийные номера: {incorrect_serials}"
    )

@dp.message(Command('name'))
async def name_entrypoint(
    message: types.Message,
    state: FSMContext
):
    await message.answer('Отправьте имя')
    await state.set_state(StGroup.name)

@dp.message(NameFilter(), StGroup.name)
async def name_message(
    message: types.Message,
    state: FSMContext,
    name: list
):
    await message.answer(f"Ваше имя: {name}")
    await state.clear()


async def main():
    try:
        await dp.start_polling(bot,
                               allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())