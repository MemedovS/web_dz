from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bots.user_steps_manager import save_step
from bots.user_steps_manager import create_keyboard
from bots.ip_tv_text import *

router1 = Router()


# Обработчик команды /internet_problems
@router1.message(Command("iptv"))
async def iptv_prob(message: types.Message):
    buttons = [
        InlineKeyboardButton(text="Проблемы с ip-tv ", callback_data="ipt_problems")
    ]
    keyboard = create_keyboard(buttons)
    await message.answer("Выберите действие:", reply_markup=keyboard)


@router1.callback_query(lambda c: c.data == "ipt_problems")
async def ipt_problems(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "ipt_problems")
    buttons = [
        InlineKeyboardButton(text="Есть авария", callback_data="issue_exists"),
        InlineKeyboardButton(text="Нет аварий", callback_data="no_issues_tv"),

    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "<b>1.Проверяем статус клиента в биллинге.\n2. ПРОВЕРЯЕМ ЧАТ АВАРИИ.</b>",reply_markup=keyboard,parse_mode="HTML"
    )
    await callback.answer()


# Обработчик кнопки "Нет аварий"
@router1.callback_query(lambda c: c.data == "no_issues_tv")
async def no_issues_tv(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "no_issues_tv")  # Сохраняем шаг
    buttons = [
        InlineKeyboardButton(text="IP TV не работает", callback_data="ip_tv_doesnt_work"),
        InlineKeyboardButton(text="IP TV работает медленно"
                                  " или не показывает часть каналов", callback_data="ip_tv_slow_channels"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        # InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "<b>Смотрим статус абонента,"
        " нет ли блокировок по недостатку"
        " денежных средств:</b>", reply_markup=keyboard,parse_mode="HTML")
    await callback.answer()


@router1.callback_query(lambda c: c.data == "ip_tv_doesnt_work")
async def ip_tv_doesnt_work(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "ip_tv_doesnt_work")  # Сохраняем шаг
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{ip_t_doesnt_work}", reply_markup=keyboard,parse_mode="HTML")
    await callback.answer()


@router1.callback_query(lambda c: c.data == "ip_tv_slow_channels")
async def ip_tv_slow_channels(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "ip_tv_slow_channels")  # Сохраняем шаг
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{ip_tv_slow_channel}", reply_markup=keyboard,parse_mode="HTML")
    await callback.answer()

