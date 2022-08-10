import os

import telebot
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from telebot import types


class Command(BaseCommand):
    help = "telegram-bot"
    print(os.environ["BOT_API"])

    def handle(self, *args, **options):
        bot = telebot.TeleBot(os.environ["BOT_API"])

        valid_users = {
            "bogdan": 1799244985,
            "lovelas": 1836086969,
            "serg_leonenko": 493498763,
        }

        @bot.message_handler(commands=["start"])
        def start(message):
            bot.send_message(
                message.chat.id,
                "Hello!\npush this <b>/button</b> command",
                parse_mode="html",
            )

        @bot.message_handler(commands=["button"])
        def button_message(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Registration")
            markup.add(item1)
            bot.send_message(message.chat.id, "Push registration", reply_markup=markup)

        @bot.message_handler(content_types=["text"])
        def message_reply(message):
            username = message.from_user.username
            user_id = message.from_user.id
            if message.text == "Registration":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Get credentials")
                markup.add(item1)
                if user_id in valid_users.values():
                    user, created = get_user_model().objects.get_or_create(
                        username=username
                    )
                    if created:
                        user.set_password(str(user_id))
                        user.save()
                        bot.send_message(
                            message.chat.id,
                            "Registration successfully!",
                            reply_markup=markup,
                        )
                    elif user:
                        bot.send_message(
                            message.chat.id,
                            "You've already registered!",
                            reply_markup=markup,
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        "You can't be registered, credentials are not valid",
                    )
            elif message.text == "Get credentials":
                inline_markup = types.InlineKeyboardMarkup()
                inline_markup.add(
                    types.InlineKeyboardButton(
                        "Go to the website...",
                        url="http://127.0.0.1:8000/accounts/login/",
                    )
                )
                bot.send_message(
                    message.chat.id,
                    f"'username': {username}\n'password': {user_id}\n🚀",
                    reply_markup=inline_markup,
                )

        bot.infinity_polling()
        bot.polling(none_stop=True)
