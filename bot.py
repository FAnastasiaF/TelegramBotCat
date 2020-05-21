import telebot
import random
import time
import cat_lists
import copy


bot = telebot.TeleBot(TOKEN)


keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Викторина на знание пород кошек', 'Хочу фото котика', 'Хочу стикер с котиком')


def sendquiz(message):
    listkeys = copy.deepcopy(cat_lists.CATS_BREEDS)
    results = 0
    for i in range(10):
        optionslist = []
        for j in range(4):
            optionslist.append(listkeys[random.randint(0, len(listkeys)-1)])
            listkeys.remove(optionslist[j])
        correct_option = random.randint(0, 3)
        bot.send_photo(chat_id=message.chat.id,
                       photo=open(optionslist[correct_option]+".jpg", "rb"),
                       disable_notification=True)
        messagebot = bot.send_poll(chat_id=message.chat.id,
                                   question="{}.Какая порода?".format(i+1),
                                   options=optionslist,
                                   is_anonymous=False,
                                   type='quiz',
                                   correct_option_id=correct_option,
                                   disable_notifications=True)
        time.sleep(15)
        results += ((bot.stop_poll(message.chat.id, messagebot.message_id).options)[correct_option]).voter_count
    bot.send_message(message.chat.id,
                     "Ваш результат {}".format(results),
                     disable_notification=True)
    bot.send_sticker(message.chat.id,
                     'CAACAgIAAxkBAAIB8F7BktT62mUSxUeWQ5QctofWrq9MAAIGAQACb6yABWdriq2vK9y-GQQ',
                     disable_notification=True)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет, ты написал мне!',
                     reply_markup=keyboard1)
    bot.send_sticker(message.chat.id,
                     'CAACAgIAAxkBAAICEl7BlHGOjNsjU1ZYzxK0fS8LSbgnAAIcAQACb6yABRwmSBsqSiohGQQ',
                     disable_notification=True)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Я умею:\n'
                                      'Устраивать викторину'
                                      '[напиши мне или нажми на кнопку \'Викторина на знание пород кошек\']\n'
                                      'Присылать фото кота по его породе'
                                      '[напиши мне породу]\n'
                                      'Прислать фото котика'
                                      '[напиши мне или нажми на кнопку \'Хочу фото котика\']\n'
                                      'Прислать стикер с котиком'
                                      '[напиши мне или нажми на кнопку \'Хочу стикер с котиком\']\n'
                                      'Если ты мне отправишь стикер я отправлю тебе его же',
                     reply_markup=keyboard1,
                     disable_notification=True)

@bot.message_handler(content_types = ['text'])
def text(message):
    if(message.text == 'Викторина на знание пород кошек'):
        sendquiz(message)
    elif(message.text in cat_lists.CATS_BREEDS):
        bot.send_photo(message.chat.id,
                       open(message.text + ".jpg", "rb"),
                       reply_markup=keyboard1,
                       disable_notification=True)
    elif(message.text == 'Хочу фото котика'):
        bot.send_photo(message.chat.id,
                       open(cat_lists.CATS_BREEDS[random.randint(0, len(cat_lists.CATS_BREEDS)-1)] + ".jpg", 'rb'),
                       reply_markup=keyboard1,
                       disable_notification=True)
    elif(message.text == 'Хочу стикер с котиком'):
        bot.send_sticker(message.chat.id,
                         cat_lists.CAT_STICKERS[random.randint(0, len(cat_lists.CAT_STICKERS) - 1)],
                         reply_markup=keyboard1,
                         disable_notification=True)
    else:
        bot.send_message(message.chat.id,
                         'Я такого не знаю',
                         reply_markup=keyboard1,
                         disable_notification=True)

@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    bot.send_sticker(message.chat.id,
                     message.sticker.file_id,
                     disable_notification=True)


bot.polling(none_stop=True)
