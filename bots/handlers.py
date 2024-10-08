from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bots.internet_problems_text import *
from bots.internet_disconect import *
from bots.user_steps_manager import save_step, get_previous_step, create_keyboard
from bots.iptv import ipt_problems, no_issues_tv, ip_tv_doesnt_work
from bots.ktv import kt_problems, no_issues_ktv, k_tv_doesnt_work, k_tv_disconect

router = Router()


@router.callback_query(lambda c: c.data == "go_back")
async def go_back(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    previous_step = get_previous_step(user_id)

    if previous_step:
        handler = STEP_HANDLERS.get(previous_step)
        if handler:
            await handler(callback)
        else:
            await callback.answer("Не удалось определить предыдущий шаг.")
    else:
        await callback.answer("Нет доступных шагов для возврата.")


# Обработчик команды /старт
@router.message(Command("start"))
async def intern_prob(message: types.Message):
    save_step(message.from_user.id, "start")
    buttons = [
        InlineKeyboardButton(text="Проблемы с интернетом", callback_data="internet"),
        InlineKeyboardButton(text="iptv_problems", callback_data="iptv_problems")

    ]
    keyboard = create_keyboard(buttons)
    await message.answer("Выберите действие:", reply_markup=keyboard)


# Обработчик команды /internet_problems
@router.message(Command("internet"))
async def internet_prob(message: types.Message):
    buttons = [
        InlineKeyboardButton(text="Проблемы с интернетом<", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await message.answer("<b><i>Выберите действие:</i></b>", reply_markup=keyboard,parse_mode="HTML")


# Обработчик для "Проблемы с интернетом"
@router.callback_query(lambda c: c.data == "internet_problems")
async def internet_problems(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "internet_problems")  # Сохраняем шаг
    buttons = [
        InlineKeyboardButton(text="Есть авария", callback_data="issue_exists"),
        InlineKeyboardButton(text="Нет аварий", callback_data="no_issues"),
        # InlineKeyboardButton(text="Назад", callback_data="go_back"),# Добавляем кнопку "Назад"
        # InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "<b><i>1. Проверяем статус клиента в биллинге.\n2. ПРОВЕРЯЕМ ЧАТ АВАРИИ.</i></b>",
        reply_markup=keyboard,parse_mode="HTML"
    )
    await callback.answer()


# Обработчик кнопки "Есть авария"
@router.callback_query(lambda c: c.data == "issue_exists")
async def issue_exists(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "issue_exists")  # Сохраняем шаг
    buttons = [

        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        # nlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "<b><i>Приносим извинения за доставленные неудобства. Пожалуйста, подождите решения проблемы.</i></b>",
        reply_markup=keyboard,parse_mode="HTML"
    )
    await callback.answer()


# Обработчик кнопки "Нет аварий"
@router.callback_query(lambda c: c.data == "no_issues")
async def no_issues(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "no_issues")  # Сохраняем шаг
    buttons = [
        InlineKeyboardButton(text="Не работает интернет", callback_data="no_internet"),
        InlineKeyboardButton(text="Интернет работает медленно", callback_data="slow_internet"),
        InlineKeyboardButton(text="Интернет разрыв соединения", callback_data="connection_issue"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("<b><i>Проводим диагностику:</i></b>", reply_markup=keyboard,parse_mode="HTML")
    await callback.answer()


# Обработчик кнопки "Не работает интернет"
@router.callback_query(lambda c: c.data == "no_internet")
async def no_internet(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "no_internet")  # Сохраняем шаг
    buttons = [
        InlineKeyboardButton(text="Диагностика PPPoE", callback_data="pppoe_diagnosis"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("<b><i>Проверяем наличие активной сессии:</i></b>", reply_markup=keyboard,parse_mode="HTML")
    await callback.answer()


# Обработчик кнопки "Диагностика PPPoE"
@router.callback_query(lambda c: c.data == "pppoe_diagnosis")
async def pppoe_diagnosis(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "pppoe_diagnosis")  # Сохраняем шаг
    buttons = [
        InlineKeyboardButton(text="Сессия есть", callback_data="session_exists"),
        InlineKeyboardButton(text="Сессия нет", callback_data="session_no"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("<b><i>Проверяем наличие активной PPPoE сессии.</i></b>", reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "Сессия есть"
@router.callback_query(lambda c: c.data == "session_exists")
async def session_exists(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "session_exists")
    buttons = [
        InlineKeyboardButton(text="Напрямую", callback_data="direct_connection"),
        InlineKeyboardButton(text="Роутер", callback_data="session_exists_router_connection"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f'{sess_exists}', reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "Напрямую"
@router.callback_query(lambda c: c.data == "direct_connection")
async def direct_connection(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "direct_connection")
    buttons = [
        InlineKeyboardButton(text="Диагностика ошибок ", callback_data="Diag_of_errors_direct_connect"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems"),
        InlineKeyboardButton(text="Назад", callback_data="go_back")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f'{direct_conn}', reply_markup=keyboard, parse_mode='HTML')
    await callback.answer()


######
# Обработчик кнопки "Диагностика напримую"
@router.callback_query(lambda c: c.data == "Diag_of_errors_direct_connect")
async def errors_direct_diagnosis(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "Diag_of_errors_direct_connect")
    buttons = [
        InlineKeyboardButton(text="Ошибка 651, 678, 815  ", callback_data="errors_651_678_815"),
        InlineKeyboardButton(text="Ошибка 691, 629, 619, 718   ", callback_data="errors_691_629_619_718"),
        InlineKeyboardButton(text="Ошибка 769, 814 ", callback_data="errors_769_814"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]

    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{Diag_of_errors_direct_con}",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "ошибка 651 678 815"
@router.callback_query(lambda c: c.data == "errors_651_678_815")
async def errors_651_678_815(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "errors_651_678_815")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]

    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{errors_815}{response_to_client}", reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "Ошибка 691, 629, 619, 718"
@router.callback_query(lambda c: c.data == "errors_691_629_619_718")
async def errors_691_629_619_718(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "errors_691_629_619_718")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{errors_718}{response_to_client}", reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "Ошибка 769, 814"
@router.callback_query(lambda c: c.data == "errors_769_814")
async def errors_769_814(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "errors_769_814")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{errors_814}{response_to_client}", reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


#######
# Обработчик кнопки "Роутер"################################################################
@router.callback_query(lambda c: c.data == "session_exists_router_connection")
async def session_exists_router_connection(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "session_exists_router_connection")
    buttons = [
        InlineKeyboardButton(text="На всех устройствах", callback_data="on_all_devices"),
        InlineKeyboardButton(text="Проблема только на ПКУточняем ", callback_data="the_problem_is_only_on_ps"),
        InlineKeyboardButton(text="Проблема на телефоне/планшете", callback_data="problem_on_phone_tablet"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{internet_prob_router_act_sesion}", reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "На всех устройствах"
@router.callback_query(lambda c: c.data == "on_all_devices")
async def on_all_devices(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "on_all_devices")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{sesion_ex_on_all_devices}{response_to_client}", reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "problem_on_phone_tablet"
@router.callback_query(lambda c: c.data == "problem_on_phone_tablet")
async def problem_on_phone_tablet(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "problem_on_phone_tablet")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="Шаблон заявки если не работает и на др устройстве",
                             callback_data="not_work_on_another_device"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{sesion_ex_problem_on_phone_tablet}", reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "Шаблон заявки если не работает и на др устройстве"
@router.callback_query(lambda c: c.data == "not_work_on_another_device")
async def not_work_on_another_device(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "not_work_on_another_device")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        f"{sesion_ex_problem_on_phone_tablet_not_work_on_another_device}{response_to_client}",
        reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "the_problem_is_only_on_ps"
@router.callback_query(lambda c: c.data == "the_problem_is_only_on_ps")
async def the_problem_is_only_on_ps(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "the_problem_is_only_on_ps")
    buttons = [
        InlineKeyboardButton(text="Пачкорд", callback_data="internet_problems_patch_cord"),
        InlineKeyboardButton(text="wi-fi", callback_data="internet_problems_wi_fi"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("<b><i>Проблема только на ПКУ точняем подключаются через вай фай или пачкордом ?</i></b>",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "internet_problems_patch_cord"
@router.callback_query(lambda c: c.data == "internet_problems_patch_cord")
async def internet_problems_patch_cord(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "internet_problems_patch_cord")
    buttons = [
        InlineKeyboardButton(text="Шаблон заявки", callback_data="application_template_patchcord"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{sesion_ex_internet_problems_patch_cord}",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "application_template_patchcord"
@router.callback_query(lambda c: c.data == "application_template_patchcord")
async def application_template_patchcord(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "application_template_patchcord")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{sesion_ex_application_template_patchcord}{response_to_client}",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "internet_problems_wi_fi"
@router.callback_query(lambda c: c.data == "internet_problems_wi_fi")
async def internet_problems_wi_fi(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "internet_problems_wi_fi")
    buttons = [
        InlineKeyboardButton(text="Шаблон заявки", callback_data="application_template_wi_fi"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{sesion_ex_internet_problems_wi_fi}",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "application_template_wi-fi"
@router.callback_query(lambda c: c.data == "application_template_wi_fi")
async def application_template_wi_fi(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "application_template_wi_fi")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{sesion_ex_application_template_wi_fi}{response_to_client}",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


################################################################################
# Обработчик кнопки "Сессия нет"
@router.callback_query(lambda c: c.data == "session_no")
async def session_no(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "session_no")

    buttons = [
        InlineKeyboardButton(text="проверка роутера", callback_data="no_session_checking_the_router"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("<b><i>Сессии нет:"
                                     "Уточняем у клиента Как вы подключаетесь?"
                                     "напрямую от кабеля или через вайфай роутер?</i></b>",
        reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "проверка роутера""
@router.callback_query(lambda c: c.data == "no_session_checking_the_router")
async def no_session_checking_the_router(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "no_session_checking_the_router")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{no_session_checking_router}\n{response_to_client}",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


###########################################################
# Обработчик кнопки "Интернет работает медленно"
@router.callback_query(lambda c: c.data == "slow_internet")
async def slow_internet(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "slow_internet")
    buttons = [
        InlineKeyboardButton(text="Напрямую", callback_data="direct_connection_speed"),
        InlineKeyboardButton(text="Через роутер", callback_data="router_connection_speed"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("<b><i>Уточняем у клиента: Как вы подключаетесь, напрямую или через роутер?</i></b>",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "Напрямую" при замерах скорости
@router.callback_query(lambda c: c.data == "direct_connection_speed")
async def direct_connection_speed(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "direct_connection_speed")
    buttons = [
        InlineKeyboardButton(text="Клиент согласен сделать замеры", callback_data="client_agrees_speed_test"),
        InlineKeyboardButton(text="Клиент  не согласен сделать замеры", callback_data="client_agrees_no_speed_test"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f'{direct_connec_speed}', reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


@router.callback_query(lambda c: c.data == "client_agrees_no_speed_test")
async def client_agrees_no_speed_test(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "client_agrees_no_speed_test")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),

        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f'{client_agre_no_spe_test}{response_to_client}\n', reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Клиент согласен сделать замеры"
@router.callback_query(lambda c: c.data == "client_agrees_speed_test")
async def client_agrees_speed_test(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "client_agrees_speed_test")
    buttons = [
        InlineKeyboardButton(text="Скорость соответствует тарифу", callback_data="speed_matches_tariff"),
        InlineKeyboardButton(text="Скорость не соответствует тарифу", callback_data="speed_does_not_match_tariff"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "<b><i>Смотрим результаты замеров. Какова скорость?\nСкорость соответствует вашему тарифу?</i></b>",
        reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "Скорость соответствует тарифу"
@router.callback_query(lambda c: c.data == "speed_matches_tariff")
async def speed_matches_tariff(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "speed_matches_tariff")
    buttons = [
        InlineKeyboardButton(text="Клиент настаивает на заявке", callback_data="client_insists_on_request"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f'{speed_matches_tarif}', reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "Клиент настаивает на заявке"
@router.callback_query(lambda c: c.data == "client_insists_on_request")
async def client_insists_on_request(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "client_insists_on_request")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]

    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{client_insists_on_reques}{response_to_client}",
                                     reply_markup=keyboard,parse_mode='HTML'
                                     )
    await callback.answer()


# Обработчик кнопки "Скорость не соответствует тарифу"
@router.callback_query(lambda c: c.data == "speed_does_not_match_tariff")
async def speed_does_not_match_tariff(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "speed_does_not_match_tariff")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{speed_does_not_match_tarif}{response_to_client}",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


############################################################################
# Обработчик кнопки "Роутер"
@router.callback_query(lambda c: c.data == "router_connection_speed")
async def router_connection_speed(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "router_connection_speed")
    buttons = [
        InlineKeyboardButton(text="Согласен подключиться патч-кордом", callback_data="agree_patch_cord"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f'{router_connection_spe}', reply_markup=keyboard,parse_mode='HTML'
                                     )
    await callback.answer()


# Обработчик кнопки "Согласен подключиться патч-кордом"
@router.callback_query(lambda c: c.data == "agree_patch_cord")
async def agree_patch_cord(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "agree_patch_cord")
    buttons = [
        InlineKeyboardButton(text="Клиент согласен сделать замеры", callback_data="client_agrees_speed_test_router"),
        InlineKeyboardButton(text="Клиент НЕ согласен сделать замеры", callback_data="client_refuses_speed_test"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f'{agree_patch_cor}',
                                     reply_markup=keyboard,parse_mode='HTML'
                                     )
    await callback.answer()


# Обработчик кнопки "Клиент согласен сделать замеры" для роутера
@router.callback_query(lambda c: c.data == "client_agrees_speed_test_router")
async def client_agrees_speed_test_router(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "client_agrees_speed_test_router")
    buttons = [
        InlineKeyboardButton(text="Скорость соответствует тарифу", callback_data="speed_matches_tariff_router"),
        InlineKeyboardButton(text="Скорость не соответствует тарифу",
                             callback_data="speed_does_not_match_tariff_router"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("<b><i>1. Заходим с клиентом на сайт спид тест и делаем замеры скорости\n\n2."
                                     " Смотрим какая у клиента скорость по тарифу, если отклонение СКОЛЬКО% ?"
                                     "то Скорость соответствует тарифу , если более то нет.</i></b>",

        reply_markup=keyboard,parse_mode='HTML'
    )
    await callback.answer()


# Обработчик кнопки "Скорость соответствует тарифу" для роутера
@router.callback_query(lambda c: c.data == "speed_matches_tariff_router")
async def speed_matches_tariff_router(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "speed_matches_tariff_router")
    buttons = [
        InlineKeyboardButton(text="Клиент настаивает на заявке", callback_data="client_insists_on_request_router"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("<b><i>Скорость соответствует заявленной. Вероятно, проблема в вашем компьютере.\n"
                                    "Если клиент настаивает на заявке, её можно оформить.</i></b>",reply_markup=keyboard,parse_mode='HTML'
    )
    await callback.answer()


# Обработчик кнопки "Клиент настаивает на заявке" для роутера
@router.callback_query(lambda c: c.data == "client_insists_on_request_router")
async def client_insists_on_request_router(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "client_insists_on_request_router")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"<b><i>Заявка создана:"
                                     f"Низкая скорость интернета, клиент подключается через роуте"
                                     f" замеры выполнены через патч-корд."
                                     f"Скорость соответствует тарифу, но клиент настаивает на заявке\n"
                                     f"(если клиент конфликтный то указываем это )</i></b>\n"
                                     f"{response_to_client}",
        reply_markup=keyboard,parse_mode='HTML'
    )
    await callback.answer()


# Обработчик кнопки "Скорость не соответствует тарифу" для роутера
@router.callback_query(lambda c: c.data == "speed_does_not_match_tariff_router")
async def speed_does_not_match_tariff_router(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "speed_does_not_match_tariff_router")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{
    speed_does_not_match_tariff_rout}{response_to_client}",
        reply_markup=keyboard,parse_mode='HTML'
    )
    await callback.answer()


# Обработчик кнопки "Клиент НЕ согласен сделать замеры" (конфликтный клиент)
@router.callback_query(lambda c: c.data == "client_refuses_speed_test")
async def client_refuses_speed_test(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "client_refuses_speed_test")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)

    await callback.message.edit_text(f"{client_refuses_speed_tes }{response_to_client}",  # Merge into the f-string
        reply_markup=keyboard,parse_mode='HTML'
    )

    await callback.answer()


###########
# Обработчик кнопки "Интернет разрыв соединения"
@router.callback_query(lambda c: c.data == "connection_issue")
async def connection_issue(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "connection_issue")
    buttons = [
        InlineKeyboardButton(text="Напрямую", callback_data="connection_issue_direct_connection"),
        InlineKeyboardButton(text="Роутор", callback_data="connection_issue_router_connection"),
        InlineKeyboardButton(text="Уже наблюдал розрыв при подключении",
                             callback_data="connection_issue_er_connection"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("Интернет разрывы соединенияУточняем у клиента: "
                                     "Скажите пожалуйста как вы подключаетесь "
                                     "напрямую или через роутер?.",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "напрямую"
@router.callback_query(lambda c: c.data == "connection_issue_direct_connection")
async def connect_issue_direct_connec(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "connection_issue_direct_connection")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{connection_issue_direct_connection}\n {response_to_client}",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "router"
@router.callback_query(lambda c: c.data == "connection_issue_router_connection")
async def connec_issue_router_connection(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "connection_issue_router_connection")
    buttons = [
        InlineKeyboardButton(text="На всех устройствах", callback_data="connection_issue_router_on_all_devices"),
        InlineKeyboardButton(text="Только на одном", callback_data="connection_issue_router_on_devices"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("Уточняем у клиента на всех ли устройствах отслеживаются разрывы соединения ?",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "На всех устройствах"
@router.callback_query(lambda c: c.data == "connection_issue_router_on_all_devices")
async def connec_issue_router_on_all_devices(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "connection_issue_router_on_all_devices")
    buttons = [
        InlineKeyboardButton(text="Клиент отказывается/конфликтует",
                             callback_data="connection_issue_router_the_client_conflicts"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{connect_issue_router_on_all_devices}", reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "Клиент отказывается/конфликтует"
@router.callback_query(lambda c: c.data == "connection_issue_router_the_client_conflicts")
async def connec_issue_router_the_client_conflicts(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "connection_issue_router_the_client_conflicts")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{connec_issue_router_the_client_conflic}{response_to_client}",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "Только на одном"
@router.callback_query(lambda c: c.data == "connection_issue_router_on_devices")
async def connect_issue_router_on_devic(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "connection_issue_router_on_devices")
    buttons = [
        InlineKeyboardButton(text="Клиент отказывается/конфликтует",
                             callback_data="connection_issue_router_on_devices_client_conflicts"),
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{conne_issue_router_on_devic}", reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "Клиент отказывается/конфликтует"
@router.callback_query(lambda c: c.data == "connection_issue_router_on_devices_client_conflicts")
async def connecti_issue_router_on_device_client_conflicts(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "connection_issue_router_on_devices_client_conflicts")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{connec_issue_router_the_client_conflic}\n{response_to_client}",
                                     reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


# Обработчик кнопки "Уже наблюдал розрыв при подключении"
@router.callback_query(lambda c: c.data == "connection_issue_er_connection")
async def connect_issue_er_connect(callback: types.CallbackQuery):
    save_step(callback.from_user.id, "connection_issue_er_connection")
    buttons = [
        InlineKeyboardButton(text="Назад", callback_data="go_back"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{connec_issue_er_connect}\n{response_to_client}",
                                     reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


STEP_HANDLERS = {

    "internet_problems": internet_problems,
    "no_issues": no_issues,
    "no_internet": no_internet,
    "pppoe_diagnosis": pppoe_diagnosis,
    "session_exists": session_exists,
    "direct_connection": direct_connection,
    "Diag_of_errors_direct_connect": errors_direct_diagnosis,
    "errors_651_678_815": errors_651_678_815,
    "errors_691_629_619_718": errors_691_629_619_718,
    "errors_769_814": errors_769_814,
    "session_exists_router_connection": session_exists_router_connection,
    "on_all_devices": on_all_devices,
    "problem_on_phone_tablet": problem_on_phone_tablet,
    "not_work_on_another_device": not_work_on_another_device,
    "the_problem_is_only_on_ps": the_problem_is_only_on_ps,
    "application_template_patchcord": application_template_patchcord,
    "internet_problems_patch_cord": internet_problems_patch_cord,
    "internet_problems_wi_fi": internet_problems_wi_fi,
    "application_template_wi_fi": application_template_wi_fi,
    "session_no": session_no,
    "no_session_checking_the_router": no_session_checking_the_router,
    "slow_internet": slow_internet,
    "direct_connection_speed": direct_connection_speed,
    "client_agrees_no_speed_test": client_agrees_no_speed_test,
    "client_agrees_speed_test": client_agrees_speed_test,
    "speed_matches_tariff": speed_matches_tariff,
    "client_insists_on_request": client_insists_on_request,
    "speed_does_not_match_tariff": speed_does_not_match_tariff,
    "router_connection_speed": router_connection_speed,
    "agree_patch_cord": agree_patch_cord,
    "client_agrees_speed_test_router": client_agrees_speed_test_router,
    "speed_matches_tariff_router": speed_matches_tariff_router,
    "client_insists_on_request_router": client_insists_on_request_router,
    "speed_does_not_match_tariff_router": speed_does_not_match_tariff_router,
    "client_refuses_speed_test": client_refuses_speed_test,
    "connection_issue": connection_issue,
    "connection_issue_direct_connection": connect_issue_direct_connec,
    "connection_issue_router_connection": connec_issue_router_connection,
    "connection_issue_router_on_all_devices": connec_issue_router_on_all_devices,
    "connection_issue_router_the_client_conflicts": connec_issue_router_the_client_conflicts,
    "connection_issue_router_on_devices": connect_issue_router_on_devic,
    "connection_issue_router_on_devices_client_conflicts": connecti_issue_router_on_device_client_conflicts,
    "connection_issue_er_connection": connect_issue_er_connect,
    "no_issues_tv": no_issues_tv,
    "ipt_problems": ipt_problems,  # Добавьте сюда все соответствующие шаги
    "ip_tv_doesnt_work": ip_tv_doesnt_work,
    "kt_problems": kt_problems,
    "no_issues_ktv": no_issues_ktv,
    "k_tv_doesnt_work": k_tv_doesnt_work,
    "k_tv_disconect": k_tv_disconect

}
