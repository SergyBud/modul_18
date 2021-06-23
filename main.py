import telebot
from config import keys, TOKEN
from utilite import ConvertionException, CurrencyConvertor


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы перевести валюту, введите валюту, которую хотите обменять в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \n Увидеть список доступных валют: /value'
    bot.reply_to(message, text)


@bot.message_handler(commands=['value'])
def currency(message: telebot.types.Message):
    text = "Дотупные валюты:"
    for value in keys.keys():
        text = '\n'.join((text, value, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertionException('Слишком много параметровю')

        quote, base, amount = value
        total_base = CurrencyConvertor.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()

