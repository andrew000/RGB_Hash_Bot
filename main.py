import logging
import os
from random import randint

from PIL import Image
from telegram import *
from telegram.ext import *

from core import rgb_func, config

logging.basicConfig(handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')],
                    level=logging.INFO,
                    format='[*] {%(pathname)s:%(lineno)d} %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def start(update, _):
    update.message.reply_text("Генерация цвета из никнейма\n"
                              "\n"
                              "/rgba - Формула AndrewKing\n"
                              "/rgbv - Формула Victor %\n"
                              "/rgbd - Обе формулы")


@run_async
def rgb_a(update, _):  # AndrewKing's formula
    rgb_ = rgb_func.rgb_hash_a(update.effective_user.full_name)
    filename = "{}_{}.png".format(update.effective_user.id, randint(0, 99999))
    img = Image.new('RGB', (256, 128), color=rgb_)
    img.save(filename)
    filename = os.path.abspath(filename)

    try:
        update.effective_message.reply_photo(photo=open(filename, 'rb'),
                                             caption=f"Хеш по формуле AndrewKing\n"
                                                     f"\n"
                                                     f"Имя: {update.effective_user.full_name}")

    except TelegramError:
        pass

    os.remove(filename)


@run_async
def rgb_v(update, _):  # Viktor's formula
    rgb_ = rgb_func.rgb_hash_v(update.effective_user.full_name)
    filename = "{}_{}.png".format(update.effective_user.id, randint(0, 99999))
    img = Image.new('RGB', (256, 128), color=rgb_)
    img.save(filename)
    filename = os.path.abspath(filename)

    try:
        update.effective_message.reply_photo(photo=open(filename, 'rb'),
                                             caption=f"Хеш по формуле Viktor %\n"
                                                     f"\n"
                                                     f"Имя: {update.effective_user.full_name}")

    except TelegramError:
        pass

    os.remove(filename)


@run_async
def rgb_d(update, _):  # AndrewKing's and Viktor's formulas
    rgba = rgb_func.rgb_hash_a(update.effective_user.full_name)
    rgbv = rgb_func.rgb_hash_v(update.effective_user.full_name)

    filename_a = "{}_{}.png".format(update.effective_user.id, randint(0, 99999))
    filename_v = "{}_{}.png".format(update.effective_user.id, randint(0, 99999))

    img_a = Image.new('RGB', (64, 128), color=rgba)
    img_v = Image.new('RGB', (64, 128), color=rgbv)

    img_a.save(filename_a)
    img_v.save(filename_v)

    filename_a = os.path.abspath(filename_a)
    filename_v = os.path.abspath(filename_v)

    try:
        update.effective_message.reply_media_group(media=(InputMediaPhoto(media=open(filename_a, 'rb'),
                                                                          caption="1. Формула AndrewKing\n"
                                                                                  "2. Формула Viktor %"),
                                                          InputMediaPhoto(media=open(filename_v, 'rb'))))

    except TelegramError:
        pass

    os.remove(filename_a)
    os.remove(filename_v)


def yuy(update, _):
    update.effective_message.reply_text(text=
                                        "<code>"
                                        " __________________________\n"
                                        "/ Дружочек, ты видимо не   \\\n"
                                        "| понял с кем связался.    |\n"
                                        "| Вот эта твоя манера речи |\n"
                                        "| «клоунская» меня совсем  |\n"
                                        "| не впечатляет. Давай     |\n"
                                        "| встретимся и я объясню   |\n"
                                        "| на понятном для тебя     |\n"
                                        "\ языке, языке боли.       /\n"
                                        " --------------------------\n"
                                        "        \   ^__^\n"
                                        "         \  (oo)\_______\n"
                                        "            (__)\       )\/\\\n"
                                        "                ||----w |\n"
                                        "                ||     ||\n"
                                        "</code>", parse_mode=ParseMode.HTML)


def error(update, context):
    print('Update "%s" caused error "%s"', update, context.error)
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def log(update, context):
    log_file = os.path.abspath('log.txt')
    try:
        context.bot.send_document(chat_id=update.message.chat.id, document=open(log_file, 'rb'))

    except TelegramError:
        update.message.reply_text("Файл пустой")


def main():
    updater = Updater(config.TOKEN, use_context=True, workers=4)
    dp = updater.dispatcher

    filters = ~Filters.update.edited_message & ~Filters.update.channel_post
    admin_filters = filters & Filters.user(user_id=config.ADMINS)

    dp.add_handler(CommandHandler('start', start, filters=filters))
    dp.add_handler(CommandHandler('rgba', rgb_a, filters=filters))
    dp.add_handler(CommandHandler('rgbv', rgb_v, filters=filters))
    dp.add_handler(CommandHandler('rgbd', rgb_d, filters=filters))

    dp.add_handler(CommandHandler('log', log, filters=admin_filters))

    # ERROR
    dp.add_error_handler(error)

    print('[+]: BOT STARTED')

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()
