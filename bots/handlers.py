from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bots.internet_problems_text import *
from bots.internet_disconect import *

router = Router()


# Функция для создания клавиатуры
def create_keyboard(buttons: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[button] for button in buttons]  # Каждая кнопка на отдельной строке
    )


# Обработчик команды /internet_problems
@router.message(Command("internet_problems"))
async def internet_prob(message: types.Message):
    buttons = [
        InlineKeyboardButton(text="Проблемы с интернетом", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await message.answer("Выберите действие:", reply_markup=keyboard)


# Обработчик кнопки "Проблемы с интернетом"
@router.callback_query(lambda c: c.data == "internet_problems")
async def internet_problems(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Есть авария", callback_data="issue_exists"),
        InlineKeyboardButton(text="Нет аварий", callback_data="no_issues")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("1) Проверяем статус клиента в биллинге.\n"
                                     "2) ПРОВЕРЯЕМ ЧАТ АВАРИИ.",
                                     reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Есть авария"
@router.callback_query(lambda c: c.data == "issue_exists")
async def issue_exists(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        f"Приносим извинения за доставленные неудобства."
        f" Пожалуйста, подождите решения проблемы.", reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Нет аварий"
@router.callback_query(lambda c: c.data == "no_issues")
async def no_issues(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Не работает интернет", callback_data="no_internet"),
        InlineKeyboardButton(text="Интернет работает медленно", callback_data="slow_internet"),
        InlineKeyboardButton(text="Интернет разрыв соединения", callback_data="connection_issue"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("Проводим диагностику:", reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Не работает интернет"
@router.callback_query(lambda c: c.data == "no_internet")
async def no_internet(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Диагностика PPPoE", callback_data="pppoe_diagnosis"),
        InlineKeyboardButton(text="Назад", callback_data="no_issues")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("Проверяем наличие активной сессии:", reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Диагностика PPPoE"
@router.callback_query(lambda c: c.data == "pppoe_diagnosis")
async def pppoe_diagnosis(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Сессия есть", callback_data="session_exists"),
        InlineKeyboardButton(text="Сессия нет", callback_data="session_no")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("Проверяем наличие активной PPPoE сессии...", reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Сессия есть"
@router.callback_query(lambda c: c.data == "session_exists")
async def session_exists(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Напрямую", callback_data="direct_connection"),
        InlineKeyboardButton(text="Роутер", callback_data="session_exists_router_connection")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        f"Уточняем у клиента: Как вы подключаетесь, "
        f"напрямую от кабеля который заходит с улицы/с подъезда к"
        f" ПК или через вайфай роутер?",
        reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Напрямую"
@router.callback_query(lambda c: c.data == "direct_connection")
async def direct_connection(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Диагностика ошибок ", callback_data="Diag_of_errors_direct_connect"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f'{direct_conn}' ,reply_markup=keyboard,parse_mode='HTML')
    await callback.answer()


######
# Обработчик кнопки "Диагностика напримую"
@router.callback_query(lambda c: c.data == "Diag_of_errors_direct_connect")
async def errors_direct_diagnosis(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Ошибка 651, 678, 815  ", callback_data="errors_651_678_815"),
        InlineKeyboardButton(text="Ошибка 691, 629, 619, 718   ", callback_data="errors_691_629_619_718"),
        InlineKeyboardButton(text="Ошибка 769, 814 ", callback_data="errors_769_814"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems"),
    ]

    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{Diag_of_errors_direct_con}",
        reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "ошибка 651 678 815"
@router.callback_query(lambda c: c.data == "errors_651_678_815")
async def errors_651_678_815(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]

    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{errors_815}{response_to_client}", reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Ошибка 691, 629, 619, 718"
@router.callback_query(lambda c: c.data == "errors_691_629_619_718")
async def errors_651_678_815(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{errors_718}{response_to_client}", reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Ошибка 769, 814"
@router.callback_query(lambda c: c.data == "errors_769_814")
async def errors_769_814(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{errors_814}{response_to_client}", reply_markup=keyboard)
    await callback.answer()


#######
# Обработчик кнопки "Роутер"################################################################
@router.callback_query(lambda c: c.data == "session_exists_router_connection")
async def session_exists_router_connection(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На всех устройствах", callback_data="on_all_devices"),
        InlineKeyboardButton(text="Проблема только на ПКУточняем ", callback_data="the_problem_is_only_on_ps"),
        InlineKeyboardButton(text="Проблема на телефоне/планшете", callback_data="problem_on_phone_tablet"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(internet_prob_router_act_sesion, reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "На всех устройствах"
@router.callback_query(lambda c: c.data == "on_all_devices")
async def on_all_devices(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{sesion_ex_on_all_devices}{response_to_client}", reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "problem_on_phone_tablet"
@router.callback_query(lambda c: c.data == "problem_on_phone_tablet")
async def problem_on_phone_tablet(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Шаблон заявки если не работает и на др устройстве",
                             callback_data="not_work_on_another_device"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{sesion_ex_problem_on_phone_tablet}", reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Шаблон заявки если не работает и на др устройстве"
@router.callback_query(lambda c: c.data == "not_work_on_another_device")
async def not_work_on_another_device(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        f"{sesion_ex_problem_on_phone_tablet_not_work_on_another_device}{response_to_client}",
        reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "the_problem_is_only_on_ps"
@router.callback_query(lambda c: c.data == "the_problem_is_only_on_ps")
async def the_problem_is_only_on_ps(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Пачкорд", callback_data="internet_problems_patch_cord"),
        InlineKeyboardButton(text="wi-fi", callback_data="internet_problems_wi_fi"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("Проблема только на ПКУ точняем подключаются через вай фай или пачкордом ?",
                                     reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "internet_problems_patch_cord"
@router.callback_query(lambda c: c.data == "internet_problems_patch_cord")
async def internet_problems_patch_cord(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Шаблон заявки", callback_data="application_template_patchcord"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{sesion_ex_internet_problems_patch_cord}",
                                     reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "application_template_patchcord"
@router.callback_query(lambda c: c.data == "application_template_patchcord")
async def application_template_patchcord(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{sesion_ex_application_template_patchcord}{response_to_client}",
                                     reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "internet_problems_wi_fi"
@router.callback_query(lambda c: c.data == "internet_problems_wi_fi")
async def internet_problems_wi_fi(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Шаблон заявки", callback_data="application_template_wi_fi"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{sesion_ex_internet_problems_wi_fi}",
                                     reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "application_template_wi-fi"
@router.callback_query(lambda c: c.data == "application_template_wi_fi")
async def application_template_wi_fi(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{sesion_ex_application_template_wi_fi}{response_to_client}",
                                     reply_markup=keyboard)
    await callback.answer()


################################################################################
# Обработчик кнопки "Сессия нет"
@router.callback_query(lambda c: c.data == "session_no")
async def session_no(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="проверка роутера", callback_data="no_session_checking_the_router"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "Сессии нет \n Уточняем у клиента Как вы подключаетесь?\n напрямую от кабеля или через вайфай роутер?",
        reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "проверка роутера""
@router.callback_query(lambda c: c.data == "no_session_checking_the_router")
async def no_session_checking_the_router(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{no_session_checking_router}\n{response_to_client}",
                                     reply_markup=keyboard)
    await callback.answer()


###########################################################
# Обработчик кнопки "Интернет работает медленно"
@router.callback_query(lambda c: c.data == "slow_internet")
async def slow_internet(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Напрямую", callback_data="direct_connection_speed"),
        InlineKeyboardButton(text="Через роутер", callback_data="router_connection_speed"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("Уточняем у клиента: Как вы подключаетесь, напрямую или через роутер?",
                                     reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Напрямую" при замерах скорости
@router.callback_query(lambda c: c.data == "direct_connection_speed")
async def direct_connection_speed(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Клиент согласен сделать замеры", callback_data="client_agrees_speed_test"),
        InlineKeyboardButton(text="Клиент  не согласен сделать замеры", callback_data="client_agrees_no_speed_test"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "Давайте проверим скорость интернета. Просим отключить все скачивания, загрузки и VPN.\n"
        "Потом зайдите на сайт Speedtest и нажмите кнопку для начала теста.\n"
        "Если нужно, помогу вам.",
        reply_markup=keyboard)
    await callback.answer()


@router.callback_query(lambda c: c.data == "client_agrees_no_speed_test")
async def client_agrees_no_speed_test(callback: types.CallbackQuery):
    buttons = [

        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f'{client_agre_no_spe_test}{response_to_client}\n', reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Клиент согласен сделать замеры"
@router.callback_query(lambda c: c.data == "client_agrees_speed_test")
async def client_agrees_speed_test(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Скорость соответствует тарифу", callback_data="speed_matches_tariff"),
        InlineKeyboardButton(text="Скорость не соответствует тарифу", callback_data="speed_does_not_match_tariff"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "Смотрим результаты замеров. Какова скорость?\n"
        "Скорость соответствует вашему тарифу?",
        reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Скорость соответствует тарифу"
@router.callback_query(lambda c: c.data == "speed_matches_tariff")
async def speed_matches_tariff(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Клиент настаивает на заявке", callback_data="client_insists_on_request"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "Скорость соответствует заявленной. Возможно, причина проблемы в вашем компьютере. "
        "Если клиент настаивает на заявке, можно её создать.",
        reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Клиент настаивает на заявке"
@router.callback_query(lambda c: c.data == "client_insists_on_request")
async def client_insists_on_request(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]

    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        f"*Заявка создана:*\n"
        f"Низкая скорость интернета, клиент подключается напрямую.\n"
        f"Сделаны замеры ping, download и upload.\n"
        f"Скорость соответствует заявленной, но клиент настаивает на заявке.\n\n"
        f"Скорость соответствует заявленной, но клиент настаивает на заявке "
        f"(если клиент конфликтный, то указываем это).\n\n"
        f"{response_to_client}",
        reply_markup=keyboard

    )
    await callback.answer()


# Обработчик кнопки "Скорость не соответствует тарифу"
@router.callback_query(lambda c: c.data == "speed_does_not_match_tariff")
async def speed_does_not_match_tariff(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        f"Да, скорость действительно не соответствует заявленной."
        f"Для решения этого вопроса оставим заявку.\n"
        f"Назовите, пожалуйста, ваш контактный номер телефона.\n"
        f"Заявка создана:\n"
        f"Низкая скорость интернета, клиент подключается через роутер,\n"
        f"замеры выполнены через патч-корд.\n"
        f"Скорость соответствует тарифу, но клиент настаивает на заявке.(если клиент конфликтный то указываем это )\n\n"
        f"{response_to_client}",

        reply_markup=keyboard)
    await callback.answer()


############################################################################
# Обработчик кнопки "Роутер"
@router.callback_query(lambda c: c.data == "router_connection_speed")
async def router_connection(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Согласен подключиться патч-кордом", callback_data="agree_patch_cord"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "!!! Очень важно объяснить клиенту, насколько важно делать замеры при подключении напрямую или патч-кордом. "
        "Если мы делаем замеры через Wi-Fi, они будут заведомо неверными. Скорость зависит от многих факторов: "
        "мощность роутера, удаленность от него, состояние устройства и т.д. При замерах без кабеля отклонения могут быть значительными.\n\n"
        "Есть ли возможность подключиться напрямую кабелем для замеров?",
        reply_markup=keyboard
    )
    await callback.answer()


# Обработчик кнопки "Согласен подключиться патч-кордом"
@router.callback_query(lambda c: c.data == "agree_patch_cord")
async def agree_patch_cord(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Клиент согласен сделать замеры", callback_data="client_agrees_speed_test_router"),
        InlineKeyboardButton(text="Клиент НЕ согласен сделать замеры", callback_data="client_refuses_speed_test"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "Давайте проверим скорость интернета. Пожалуйста, отключите все скачивания, загрузки и VPN.\n"
        "Зайдите на сайт Speedtest и нажмите кнопку для начала теста.\n"
        "Если потребуется помощь, я помогу вам.",
        reply_markup=keyboard
    )
    await callback.answer()


# Обработчик кнопки "Клиент согласен сделать замеры" для роутера
@router.callback_query(lambda c: c.data == "client_agrees_speed_test_router")
async def client_agrees_speed_test_router(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Скорость соответствует тарифу", callback_data="speed_matches_tariff_router"),
        InlineKeyboardButton(text="Скорость не соответствует тарифу",
                             callback_data="speed_does_not_match_tariff_router"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "1) Заходим с клиентом на сайт спид тест и делаем замеры скорости\n\n"
        "2) Смотрим какая у клиента скорость по тарифу, если отклонение СКОЛЬКО% ?"
        " то Скорость соответствует тарифу , если более то нет.",

        reply_markup=keyboard
    )
    await callback.answer()


# Обработчик кнопки "Скорость соответствует тарифу" для роутера
@router.callback_query(lambda c: c.data == "speed_matches_tariff_router")
async def speed_matches_tariff_router(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Клиент настаивает на заявке", callback_data="client_insists_on_request_router"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        "Скорость соответствует заявленной. Вероятно, проблема в вашем компьютере.\n"
        "Если клиент настаивает на заявке, её можно оформить.",
        reply_markup=keyboard
    )
    await callback.answer()


# Обработчик кнопки "Клиент настаивает на заявке" для роутера
@router.callback_query(lambda c: c.data == "client_insists_on_request_router")
async def client_insists_on_request_router(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        f"Заявка создана:"
        f" Низкая скорость интернета, клиент подключается через роутер,"
        f" замеры выполнены через патч-корд. "
        f"Скорость соответствует тарифу, но клиент настаивает на заявке.(если клиент конфликтный то указываем это )"
        f"{response_to_client}",
        reply_markup=keyboard
    )
    await callback.answer()


# Обработчик кнопки "Скорость не соответствует тарифу" для роутера
@router.callback_query(lambda c: c.data == "speed_does_not_match_tariff_router")
async def speed_does_not_match_tariff_router(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(
        f'Скорость не соответствует тарифу.'
        f'Оставляем заявку для решения проблемы.\n'
        f'Пожалуйста, назовите ваш контактный номер телефона.\n\n'
        f'*Заводим заявку:*\n'
        f'Низкая скорость интернета\n'
        f'Подключается через роутер\n'
        f'Напрямую подключиться возможности нет/ клиент отказался\n'
        f'Замеры делали с телефона / планшета\n'
        f'Сделали замеры ping __ dow__ upl__\n'
        f"{response_to_client}",
        reply_markup=keyboard
    )
    await callback.answer()


# Обработчик кнопки "Клиент НЕ согласен сделать замеры" (конфликтный клиент)
@router.callback_query(lambda c: c.data == "client_refuses_speed_test")
async def client_refuses_speed_test(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)

    await callback.message.edit_text(
        f"Если клиент конфликтует и отказывается от замеров, заводим заявку с соответствующим комментарием:\n"
        f"Заводим заявку:\n"
        f"Низкая скорость интернета, подключение через роутер.\n"
        f" Клиент отказывается от диагностики и настаивает на заявке.(если клиент конфликтный то указываем это )\n"
        f"{response_to_client}",  # Merge into the f-string
        reply_markup=keyboard
    )

    await callback.answer()


###########
# Обработчик кнопки "Интернет разрыв соединения"
@router.callback_query(lambda c: c.data == "connection_issue")
async def connection_issue(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Напрямую", callback_data="connection_issue_direct_connection"),
        InlineKeyboardButton(text="Роутор", callback_data="connection_issue_router_connection"),
        InlineKeyboardButton(text="Уже наблюдал розрыв при подключении",
                             callback_data="connection_issue_er_connection"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("Интернет разрывы соединенияУточняем у клиента: "
                                     "Скажите пожалуйста как вы подключаетесь "
                                     "напрямую или через роутер?.",
                                     reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "напрямую"
@router.callback_query(lambda c: c.data == "connection_issue_direct_connection")
async def connect_issue_direct_connec(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{connection_issue_direct_connection}\n {response_to_client}",
                                     reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "router"
@router.callback_query(lambda c: c.data == "connection_issue_router_connection")
async def connec_issue_router_connection(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На всех устройствах", callback_data="connection_issue_router_on_all_devices"),
        InlineKeyboardButton(text="Только на одном", callback_data="connection_issue_router_on_devices"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text("Уточняем у клиента на всех ли устройствах отслеживаются разрывы соединения ?",
                                     reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "На всех устройствах"
@router.callback_query(lambda c: c.data == "connection_issue_router_on_all_devices")
async def connec_issue_router_on_all_devices(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Клиент отказывается/конфликтует",
                             callback_data="connection_issue_router_the_client_conflicts"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{connect_issue_router_on_all_devices}", reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Клиент отказывается/конфликтует"
@router.callback_query(lambda c: c.data == "connection_issue_router_the_client_conflicts")
async def connec_issue_router_the_client_conflicts(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{connec_issue_router_the_client_conflic}\n{response_to_client}",
                                     reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Только на одном"
@router.callback_query(lambda c: c.data == "connection_issue_router_on_devices")
async def connect_issue_router_on_devic(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="Клиент отказывается/конфликтует",
                             callback_data="connection_issue_router_on_devices_client_conflicts"),
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{conne_issue_router_on_devic}", reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Клиент отказывается/конфликтует"
@router.callback_query(lambda c: c.data == "connection_issue_router_on_devices_client_conflicts")
async def connecti_issue_router_on_device_client_conflicts(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{connec_issue_router_the_client_conflic}\n{response_to_client}",
                                     reply_markup=keyboard)
    await callback.answer()


# Обработчик кнопки "Уже наблюдал розрыв при подключении"
@router.callback_query(lambda c: c.data == "connection_issue_er_connection")
async def connect_issue_er_connect(callback: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text="На главную", callback_data="internet_problems")
    ]
    keyboard = create_keyboard(buttons)
    await callback.message.edit_text(f"{connec_issue_er_connect}\n{response_to_client}",
                                     reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
