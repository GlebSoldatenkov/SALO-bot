from loader import bot
from keyboards.reply.player import request_contact
from states.player_information import UserInfoState
from telebot.types import Message


@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Здарова!, {message.from_user.username} введи свое имя')


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Ок, записал твое имя в тетрадочку')
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Ты дурак? Имя не может содержать цифры!')


@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Ок, записал твой возраст в блокнотик')
        bot.set_state(message.from_user.id, UserInfoState.weapon, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['age'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Ты дурачина? Возраст - это цыфэрки!!')


@bot.message_handler(state=UserInfoState.weapon)
def get_age(message: Message) -> None:
    if message.text.isalpha() and len(message.text.split()) <= 2:
        bot.send_message(message.from_user.id, f'Тебе нравится {message.text}? Мне нравится твой стиль!',
                         'Теперь отправь телефон, нажав на кнопку',
                         reply_markup=request_contact())
        bot.set_state(message.from_user.id, UserInfoState.phone, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['weapon'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Какое-то странное у тебя оружие, давай другое.')


@bot.message_handler(content_types=['text', 'player'], state=UserInfoState.phone)
def get_age(message: Message) -> None:
    if message.content_type == 'player':
        # bot.send_message(message.from_user.id, 'Ок, записал твой возраст в блокнотик')
        # bot.set_state(message.from_user.id, UserInfoState.weapon, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone'] = message.contact.phone_number

            text = f'Имя - {data["name"]}\n' \
                   f'Возраст - {data["age"]}\n' \
                   f'Оружие -  {data["weapon"]}\n' \
                   f'Номер телефона - {data["phone"]}'
            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, 'Чтобы отправить инфу, нажми на кнопку!!!!')















