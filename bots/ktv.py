from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bots.user_steps_manager import save_step
from bots.user_steps_manager import create_keyboard
from bots.ip_tv_text import *

router2 = Router()


@router2.message(Command("ktv_problems"))
async def ktv_prob(message: types.Message):
    buttons = [
        InlineKeyboardButton(text="Проблемы с тв ", callback_data="kt_problems")
    ]
    keyboard = create_keyboard(buttons)
    await message.answer("Выберите действие:", reply_markup=keyboard)


@router2.callback_query(lambda c: c.data == "kt_problems")
async def kt_problems(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "kt_problems")
    buttons = [
        InlineKeyboardButton(text="Есть авария", callback_data="issue_exists"),
        InlineKeyboardButton(text="Нет аварий", callback_data="no_issues_ktv"),

    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "1) Проверяем статус клиента в биллинге.\n2) ПРОВЕРЯЕМ ЧАТ АВАРИИ.",
        reply_markup=keyboard
    )
    await callback.answer()


# Обработчик кнопки "Нет аварий"
@router2.callback_query(lambda c: c.data == "no_issues_ktv")
async def no_issues_ktv(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "no_issues_ktv")  # Сохраняем шаг
    buttons = [
        InlineKeyboardButton(text="КТВ работает плохо или не показывает часть каналов",
                             callback_data="k_tv_doesnt_work"),
        InlineKeyboardButton(text="КТВ не работает", callback_data="k_tv_disconect"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        # InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "Смотрим статус абонента,"
        " нет ли блокировок по недостатку"
        " денежных средств:", reply_markup=keyboard)
    await callback.answer()


@router2.callback_query(lambda c: c.data == "k_tv_doesnt_work")
async def k_tv_doesnt_work(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "k_tv_doesnt_work")  # Сохраняем шаг
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{k_tv_doesnt_wor}", reply_markup=keyboard)
    await callback.answer()


@router2.callback_query(lambda c: c.data == "k_tv_disconect")
async def k_tv_disconect(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "k_tv_disconect")  # Сохраняем шаг
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{k_tv_disconec}", reply_markup=keyboard)
    await callback.answer()
