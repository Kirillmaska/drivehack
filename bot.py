import traceback
from main import get_type_structure
import time
from telebot import TeleBot


bot = TeleBot(token='5712360994:AAH-wwGUc14JfEVJkt-Y7OXe4BNHrLEXUX4')
error_text = 'К сожалению произошла непредвиденная ошибка. Повторите попытку еще раз!'
hello_text = 'Привет! Чтобы узнать тип документа, отправь нам его фотографию'\
             ' в удобном для тебя формате(как файл или фотографией).'


@bot.message_handler(commands=['start'])
def start_using_bot(message):
    try:
        bot.send_message(message.chat.id, hello_text)
    except Exception:
        bot.send_message(message.chat.id, error_text)


@bot.message_handler(content_types=['photo', 'document'])
def get_types_photo(message):
    try:
        if message.photo is not None:
            file_info=bot.get_file(message.photo[-1].file_id)
            downloaded_file=bot.download_file(file_info.file_path)
            src=message.chat.id
            with open(f'{src}.jpg', 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.chat.id, get_type_structure('jpg', message.chat.id))

        elif message.document is not None:
            file_info=bot.get_file(message.document.file_id)
            x=file_info.file_path.split('.')
            if x[1] in ('jpeg', 'jpg', 'png'):
                downloaded_file=bot.download_file(file_info.file_path)
                src=message.chat.id
                with open(f'{src}.{x[-1]}', 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.send_message(message.chat.id, get_type_structure(x[-1], message.chat.id))

        else:
            bot.send_message(message.chat.id, 'К сожалению отправленный вами документ не является фотографией. '
                                              'Пожалуйста, повторите попытку ещё раз, отправив корректный файл')

    except Exception:
        bot.send_message(message.chat.id, error_text)
        print(traceback.format_exc())


if __name__ == '__main__':
     while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            time.sleep(1)