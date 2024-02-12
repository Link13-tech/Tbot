import telebot
from config import keys, TOKEN
from extensions import ApiException, ValuesConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Для начала работы введите команду боту в следующем формате:\n <имя валюты, цену которой вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты>\
<количество первой валюты>\nПример: доллар евро 15\nУвидеть список всех доступных валют команда : /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        val = message.text.split(' ')

        if len(val) != 3:
            raise ApiException('Проверьте введеную команду.')

        quote, base, amount = val

        total_base = ValuesConverter.get_price(quote, base, amount)
    except ApiException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
