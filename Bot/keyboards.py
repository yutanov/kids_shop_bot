from telegram import InlineKeyboardButton


COLOR_DICT = {
    'красный': '\U0001F534',
    'оранжевый': '\U0001F7E0',
    'зеленый': '\U0001F7E2',
    'синий': '\U0001F535',
    'желтый': '\U0001F7E1',
    'белый': '\u26AA',
    'черный': '\u26AB',
    'фиолетовый': '\U0001F7E3',
    'коричневый': '\U0001F7E4',
    'другой': '\u25CD',
}


def keyboard_button(table):
    inline_keyboard = list()
    for el in table:
        button = [InlineKeyboardButton(el[1], callback_data=el[0])]
        inline_keyboard.append(button)
    return inline_keyboard


def sizes_keyboard_button(elements):
    inline_keyboard = list()
    for el in elements:
        button = [InlineKeyboardButton(el, callback_data=el)]
        inline_keyboard.append(button)
    inline_keyboard.append([InlineKeyboardButton('\u2b05 Назад', callback_data='back')])
    return inline_keyboard


def colors_keyboard_button(elements):
    inline_keyboard = list()
    for el in elements:
        circle = COLOR_DICT[el]
        button_string = f"{el} {circle}"
        button = [InlineKeyboardButton(button_string, callback_data=el)]
        inline_keyboard.append(button)
    inline_keyboard.append([InlineKeyboardButton('\u2b05 Назад', callback_data='back')])
    return inline_keyboard


def make_color_string(colors):
    color_string = ''
    for color in colors:
        circle = COLOR_DICT[color]
        color_string += f'{color} {circle} \n'
    return color_string
