import speech_recognition as sr
import subprocess
import os
from loguru import logger


def voice_to_text(path_file):

    """
    Функция конвертирует файл .oga в .wav -> Конвертация файла .wav в текст
    :param path_file: Путь до файла .oga
    :return: Текст из файла .wav
    """

    try:

        if path_file.endswith('oga'):

            recognizer = sr.Recognizer()
            file_path_name = path_file[:-3]

            subprocess.run(['ffmpeg', '-i', file_path_name + 'oga', file_path_name + 'wav'])

            record_file = sr.AudioFile(file_path_name + 'wav')

            with record_file as rf:
                audio = recognizer.record(rf)

            os.remove(file_path_name + 'wav')
            os.remove(file_path_name + 'oga')

            try:
                result = recognizer.recognize_google(audio, language='ru-RU')
            except sr.UnknownValueError:
                logger.success(f'Сообщение не распознано или пустое')
                return '*** Извините, я не смог разобрать сообщение или оно пустое. ***'

            return result

        else:
            logger.success(f'Неверное расширение файла! Ожидается файл с расширением .ogg')
    except Exception as ex:
        logger.success(f'Ошибка: {ex}')
