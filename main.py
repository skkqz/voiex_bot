import telebot
import os
import requests
from loguru import logger
from conversion import voice_to_text


TOKEN_BOT = 'ВАШ ТОКЕН'

bot = telebot.TeleBot(token=TOKEN_BOT)

logger.add('logging.log', encoding='utf-8', rotation='10MB')


@bot.message_handler(commands=['start'])
def bot_start(message):

    bot.send_message(
        message.chat.id,
        text=f'Привет {message.from_user.username}! Очень часто бывает, '
             f'что нет возможности прослушать голосовое сообщение, но очень хочется узнать, что в нём. '
             f'Я помогу тебе решить эту проблему! Перешли мне голосовое сообщение, и я переведу его тебе в текст.'
    )


@bot.message_handler(content_types=['text'])
def user_text(message):
    logger.success(f'User: {message.chat.id}-{message.from_user.username}    ввёл текст: {message.text}')

    bot.send_message(message.chat.id, text=f'{message.from_user.username} перешли мне голосовое сообщение.')


@bot.message_handler(content_types=['voice'])
def conversion_start(message):

    """
    Функция принимает голосовое сообщение и конвертирует его в текст

    :param message: Голосовое сообщение
    :return: Конвертированный текст из аудио
    """

    logger.success(f'User: {message.chat.id}-{message.from_user.username}    Начало конвертации')

    try:

        file_info = bot.get_file(message.voice.file_id)

        path_voice = file_info.file_path
        file_path_name = os.path.basename(path_voice[:-3])

        download_voice = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN_BOT, path_voice))

        with open(f'{file_path_name}oga', 'wb') as file:
            file.write(download_voice.content)

        logger.success('#' * 50)
        result = voice_to_text(f'{file_path_name}oga')
        logger.success('#' * 50)

        logger.success(f'User: {message.chat.id}-{message.from_user.username}    Конвертация прошла успешно')

        bot.send_message(message.chat.id, text=result)

    except Exception as ex:
        logger.success(f'User: {message.chat.id}-{message.from_user.username}    Ошибка {ex}')


def main():
    logger.success('Бот включен')
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
