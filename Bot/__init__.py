#!/usr/bin/env pyt

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram import LabeledPrice
from telegram.ext import PreCheckoutQueryHandler
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, CallbackContext, MessageHandler
from telegram.ext import ConversationHandler
from database import get_id, filter_table, get_categories, get_product_detail, save_sales
from keyboards import keyboard_button, sizes_keyboard_button, colors_keyboard_button, make_color_string
import os


GENDER, PRODUCT, DETAIL, CART, CHOOSE_PRODUCT, PAY, SAVE_SIZE, SAVE_COLOR, QUANTITY, ADRESS = range(10)
CATEGORIES = get_categories()
MEDIA_ROOT = '../admin_tg_bot/media/'
PAYMENT_TOKEN = 'TOKEN'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    update.effective_message.delete()
    context.user_data['cart'] = []
    start_button = "Начнем!"
    start_text = 'Добро пожаловать!\n' \
                 'Я бот "Пузатик"!\n' \
                 'Я помогу тебе выбрать одежку для Вашего карапуза! \U0001F476'
    keyboard = [
        [
            InlineKeyboardButton(start_button, callback_data='start'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(start_text, reply_markup=reply_markup)


def help_command(update, _):
    update.message.reply_text("Используйте `/start` для запуска бота.")


def cancel_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Отмена. Для перезапуска бота нажмите /start')
    return ConversationHandler.END





def start_handler(update: Update, context: CallbackContext):
    text = 'Для кого будем подбирать вещи? Для мальчика или девочки? '
    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('Мальчик \U0001F466', callback_data='Для мальчика')],
            [InlineKeyboardButton('Девочка \U0001F467', callback_data='Для девочки')],
        ],
    )
    update.callback_query.edit_message_text(text=text, reply_markup=inline_buttons)
    return GENDER


def select_category(update: Update, context: CallbackContext):
    callback_data = update.callback_query.data
    if callback_data == 'Для мальчика' or callback_data == 'Для девочки':
        context.user_data['gender'] = callback_data
    text = 'Выберите, пожалуйста, категорию '
    buttons = keyboard_button(CATEGORIES)
    buttons.append([InlineKeyboardButton('\u2b05 Назад', callback_data='back')])
    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
    update.callback_query.edit_message_text(text=text, reply_markup=inline_buttons)
    return PRODUCT


def product_list(update: Update, context: CallbackContext):
    query = update.callback_query.data
    current_id = context.user_data['current_id']
    product_list = context.user_data['products_list']
    index = product_list.index(int(current_id))
    if query == 'next':
        try:
            next_el = product_list[index + 1]
        except IndexError:
            next_el = product_list[0]
    context.user_data['current_id'] = next_el
    return product_detail(update, context)


def products(update: Update, context: CallbackContext):
    text = "Выберите, пожалуйста, товар"
    callback_data = update.callback_query.data
    if callback_data != "back":
        context.user_data['category'] = callback_data
    elif callback_data == "back":
        update.effective_message.delete()
    category = context.user_data['category']
    gender = context.user_data['gender']
    goods = filter_table('product_product', category, gender)
    context.user_data['products_list'] = [i[0] for i in goods]
    buttons = keyboard_button(goods)
    buttons.append([InlineKeyboardButton('\u2b05 Назад', callback_data='back')])
    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
    if callback_data != 'back':
        update.callback_query.edit_message_text(text=text, reply_markup=inline_buttons)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text, reply_markup=inline_buttons,
                                 )
    return DETAIL


def oth_img_data(update: Update, context: CallbackContext, context_data):
    oth_image_button = []
    context.user_data['picture'] = 0
    picture = open(context_data['image'], 'rb')
    oth_image_button.append([InlineKeyboardButton('Еще фото \U0001F5BC', callback_data='more_img')])
    return picture, oth_image_button





def product_detail(update: Update, context: CallbackContext):
    update.effective_message.delete()
    data = update.callback_query.data
    oth_image_button = []
    if data == 'next' or data == 'back':
        # if this is view of another product
        product_id = context.user_data['current_id']
        context_data = get_product_detail(product_id)
        picture, oth_image_button = oth_img_data(update, context, context_data)
    elif data == 'more_img':
        oth_image_button.append([InlineKeyboardButton('Еще фото \U0001F5BC', callback_data='more_img')])
        product_id = context.user_data['current_id']
        context_data = get_product_detail(product_id)
        # if this is not first view of product and user wants to see other images
        try:
            i = context.user_data['picture']
            pic = os.path.join(MEDIA_ROOT, context_data['oth_images'][i])
            picture = open(pic, 'rb')
            context.user_data['picture'] += 1
        except IndexError:
            picture = open(context_data['image'], 'rb')
            context.user_data['picture'] = 0
    else:
        # if this is first view of product
        product_id = update.callback_query.data
        context.user_data['current_id'] = product_id
        context_data = get_product_detail(product_id)
        # if there are other images
        if context_data['oth_images']:
            picture, oth_image_button = oth_img_data(update, context, context_data)
        else:
            picture = open(context_data['image'], 'rb')

    context.user_data['product_data'] = context_data
    sizes = ' '.join(map(str, context_data['size']))

    colors = context_data['color']
    color_string = make_color_string(colors)

    text = f"""{context_data['title']} \n
{context_data['description']} \n
{context_data['gender']} \n
Цвета:
{color_string}
Размеры: {sizes} \n
Цена: {context_data['price']} рублей \n"""

    buttons = [
        [InlineKeyboardButton('Следующий товар \u27A1', callback_data='next')],
        [InlineKeyboardButton('В корзину  \U0001F6D2', callback_data='cart')],
        [InlineKeyboardButton('\u2b05 Назад', callback_data='back')],
    ]
    inline_keyboard = oth_image_button + buttons
    inline_buttons = InlineKeyboardMarkup(inline_keyboard)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=picture,
                           caption=text, reply_markup=inline_buttons,
                           )
    return CHOOSE_PRODUCT


def save_size(update: Update, context: CallbackContext):
    update.effective_message.delete()
    text = "Выберите размер"
    sizes_list = context.user_data['product_data']['size']
    inline_keyboard = sizes_keyboard_button(sizes_list)
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text, reply_markup=inline_buttons,
                             )
    return SAVE_SIZE


def save_color(update: Update, context: CallbackContext):
    data = update.callback_query.data
    if data != 'back':
        context.user_data['chosen_size'] = data
    text = "Выберите цвет"
    color_list = context.user_data['product_data']['color']
    inline_keyboard = colors_keyboard_button(color_list)
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    update.callback_query.edit_message_text(text=text, reply_markup=inline_buttons)
    return SAVE_COLOR


def contacts(update: Update, context: CallbackContext):
    context.user_data['chosen_color'] = update.callback_query.data
    update.effective_message.delete()
    text = "Укажите, пожалуйста, контактную информацию чтобы мы могли с Вами связаться и отправить Вам товар. Ваше " \
           "имя, номер телефона, адрес."
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             )
    return ADRESS


def cart(update: Update, context: CallbackContext):
    data = update.message.text
    context.user_data['contacts'] = data
    update.effective_message.delete()
    context_data = context.user_data['product_data']
    list_of_cart = context.user_data['cart']
    list_of_cart.append(
        {
            'id': context_data['id'],
            'title': context_data['title'],
            'size': context.user_data['chosen_size'],
            'color': context.user_data['chosen_color'],
            'price': context_data['price'],
        }
    )
    context.user_data['cart'] = list_of_cart
    text_list = ''
    cost = 0.0
    for el in list_of_cart:
        title = el['title']
        price = str(el['price'])
        cost += float(el['price'])
        text_list += f"{title} - {price} руб \n"
    total_cost = str(cost)
    text = f"""Вы добавили в корзину: \n
{text_list}
\n
Общая сумма: {total_cost} \n
"""
    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('Продолжить покупки \u27A1', callback_data='next')],
            [InlineKeyboardButton('Оплатить \U0001f4b3', callback_data='pay')],
            [InlineKeyboardButton('Очистить корзину', callback_data='clear')],
        ],
    )
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text, reply_markup=inline_buttons,
                             )
    return CART


def clear_cart(update: Update, context: CallbackContext):
    update.effective_message.delete()
    list_of_cart = context.user_data['cart']
    text_list = ''
    for i, el in enumerate(list_of_cart):
        title = el['title']
        price = el['price']
        text_list += f"Товар {i} {title} - {price} руб \n"
    context.user_data['cart'] = []
    text = "Корзина очищена"
    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('OK', callback_data='back')],
        ],
    )
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text, reply_markup=inline_buttons,
                             )
    return DETAIL


def pay(update: Update, context: CallbackContext) -> None:
    update.effective_message.delete()
    list_of_cart = context.user_data['cart']
    price = 0.0
    for i, el in enumerate(list_of_cart):
        price_of_good = float(el['price'])
        price += price_of_good
    chat_id = update.effective_chat.id
    currency = 'RUB'
    prices = [LabeledPrice("Test", int(price) * 100)]
    title = "Оплата заказа"
    description = "Платеж по заказу в боте"
    payload = "Custom-Payload"
    context.bot.send_invoice(
        chat_id, title,
        description,
        payload,
        PAYMENT_TOKEN,
        currency,
        prices,
    )
    # return PAY
    # return ConversationHandler.END


def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    save_sales(context.user_data['cart'], context.user_data['contacts'])
    context.user_data['cart'] = []
    update.message.reply_text("Спасибо за покупку!")
    return ConversationHandler.END


def precheckout_callback(update: Update, context: CallbackContext) -> None:
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)


if __name__ == '__main__':
    updater = Updater("TOKEN")

    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_handler, pattern='^' + 'start' + '$'),
        ],
        states={
            GENDER: [
                CallbackQueryHandler(select_category),
            ],
            PRODUCT: [
                CallbackQueryHandler(start_handler, pattern='^' + 'back' + '$'),
                CallbackQueryHandler(products),
            ],
            DETAIL: [
                CallbackQueryHandler(select_category, pattern='^' + 'back' + '$'),
                CallbackQueryHandler(product_detail),
            ],
            CHOOSE_PRODUCT: [
                CallbackQueryHandler(product_detail, pattern='^' + 'more_img' + '$'),
                CallbackQueryHandler(products, pattern='^' + 'back' + '$'),
                CallbackQueryHandler(save_size, pattern='^' + 'cart' + '$'),
                CallbackQueryHandler(product_list, pattern='^' + 'next' + '$'),
            ],
            CART: [
                CallbackQueryHandler(select_category, pattern='^' + 'next' + '$'),
                CallbackQueryHandler(clear_cart, pattern='^' + 'clear' + '$'),
                CallbackQueryHandler(pay, pattern='^' + 'pay' + '$'),
            ],
            SAVE_SIZE: [
                CallbackQueryHandler(product_detail, pattern='^' + 'back' + '$'),
                CallbackQueryHandler(save_color),
            ],
            SAVE_COLOR: [
                CallbackQueryHandler(save_size, pattern='^' + 'back' + '$'),
                CallbackQueryHandler(contacts),
            ],
            ADRESS : [
                MessageHandler(Filters.all, cart),
            ]
        },
        allow_reentry=True,
        fallbacks=[
            CommandHandler('start', start),
            CommandHandler('help', help_command),
            CommandHandler('cancel', cancel_handler),
        ],
    )

    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler('cancel', cancel_handler))

    # Pre-checkout handler to final check
    updater.dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    updater.dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))

    updater.start_polling()
    updater.idle()
