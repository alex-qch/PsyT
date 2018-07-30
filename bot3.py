import telebot
import config

bot = telebot.TeleBot(config.token)

res_arr = dict()

keyboard = telebot.types.InlineKeyboardMarkup()
button_minus = telebot.types.InlineKeyboardButton(text='нет', callback_data='0')
button_plus = telebot.types.InlineKeyboardButton(text='да', callback_data='1')
keyboard.add(button_minus,button_plus)

testtext = []
with open('test.txt', 'r') as file:
    for row in file.readlines():
        testtext.append(row.strip())


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id, text='Диагностика фрустированности\n\nОзнакомившись с последующими ситуациями,'
                                                'дайте ответ, согласны вы с ними (поставьте рядом с номером знак «плюс») или нет (поставьте знак'
                                                '«минус»).\n\nОтправьте /begin когда будете готовы')


@bot.message_handler(commands=['begin'])
def test_handler(message):
    res_arr[message.from_user.id] = [0, 0, 0, 0]
    bot.send_message(message.from_user.id, testtext[0], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    ind = testtext.index(call.message.text) + 1
    result = call.data 
    res_arr[call.from_user.id][0] += int(result)
    try:
        bot.edit_message_text(testtext[ind], call.from_user.id, message_id=call.message.message_id, reply_markup=keyboard)
    except IndexError:
        h = round(res_arr[call.from_user.id][0])
        if h <= 4:
           mes = 'поздравляем, у вас фрустрация отсутствует! Вы набрали всего {} балла! \nЧтобы повторить, нажмите /start'.format(str(h))
        elif h >= 5 and h <= 9: 
           mes = 'У вас имеется устойчивая тенденция к фрустрации! Вы набрали {} баллов! \nЧтобы повторить, нажмите /start'.format(str(h))
        elif h >= 10 and h <= 12: 
           mes = 'У вас имеется наблюдается высокая степень фрустрации! Вы набрали {} баллов! \nЧтобы повторить, нажмите /start'.format(str(h))

        bot.edit_message_text(mes, call.from_user.id, message_id=call.message.message_id)

        del res_arr[call.from_user.id]

bot.polling(none_stop=True)
