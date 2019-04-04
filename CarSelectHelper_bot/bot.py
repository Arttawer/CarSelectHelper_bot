import os
import sys

import telegram
from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler, Filters

from car import Car
from menu import *


class Bot:

    def __init__(self):
        self.cars = []
        self.handlers = []
        self.token = open('token.txt', 'r').readline().strip()
        self.filtered_cars = []

        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.read_cars_db('cars.csv')
        self.set_handlers()
        self.register_handlers()

    def read_cars_db(self, db_file):
        cars_db = open(db_file, 'r').readlines()

        for i in cars_db[1:]:
            self.cars.append(Car(*i.strip().split(',')))

    def print_cars(self):
        for i in self.cars:
            print(i)

    def register_handlers(self):
        for handler in self.handlers:
            self.dispatcher.add_handler(handler)

    def set_handlers(self):
        self.handlers = [
            CommandHandler('start', self.start),
            ConversationHandler(
                entry_points=[MessageHandler(Filters.regex('^Найти машину$'), self.start_finding_car)],
                states={
                    0: [MessageHandler(Filters.text, self.register_carcass)],
                    1: [MessageHandler(Filters.text, self.register_consumption)],
                    2: [MessageHandler(Filters.text, self.register_min_cost)],
                    3: [MessageHandler(Filters.text, self.register_max_cost)]
                },
                fallbacks=[CommandHandler('cancel', self.cancel)]
            )
        ]

    def start(self, update, context):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="👋 Привет!\nЯ помогу тебе выбрать машину по заданным параметрам.\n👉 Чтобы начать жми "
                                      "'Найти машину'",
                                 reply_markup=main_menu)

    def start_finding_car(self, update, context):
        self.filtered_cars = self.cars
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="🚙 Выбери тип кузова" + '\n' +
                                      "1. Седан" + '\n' +
                                      "2. Купэ" + '\n' +
                                      "3. Универсал" + '\n' +
                                      "4. Внедорожник" + '\n' +
                                      "5. Хэтчбек" + '\n' +
                                      "6. Кабриолет" + '\n' +
                                      "7. Минивэн" + '\n',
                                 reply_markup=carcass_menu)
        context.bot.send_photo(chat_id=update.message.chat_id,
                               photo=open('kuzovva.jpg', 'rb'))
        return 0

    def register_carcass(self, update, context):
        def next_text():
            return "⛽ Теперь нужно определиться с расходом на 100 км:\n" \
                   "1. До 8 л\n" \
                   "2. До 10 л\n" \
                   "3. До 13 л\n" \
                   "4. До 15 л\n" \
                   "5. Больше 15\n"

        carcass = update.message.text.strip()
        if carcass in Car.possible_carcass:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="Принято, хороший кузов\n" + next_text(),
                                     reply_markup=consumption_menu
                                     )
            self.filtered_cars = list(filter(lambda x: x.carcass == carcass, self.filtered_cars))
            # print(list(self.filtered_cars))
            return 1
        elif carcass == 'Не важно':
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="Ясно, двигаемся дальше\n" + next_text(),
                                     reply_markup=consumption_menu
                                     )
            return 1
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="В моей базе такого кузова нет.\nПопробуй выбрать другой")
            return 0

    def register_consumption(self, update, context):
        def next_text():
            return "Так и запишу\n" \
                   "💵 Дальше - лучше, минимальная цена:\n" \
                   '1. от 800 т.р\n' \
                   '2. от 1 млн. р\n' \
                   '3. от 1,5 млн. р\n' \
                   '4. от 2 млн. р\n' \
                   '5. от 3 млн. р\n' \
                   '6. от 4 млн. р\n' \
                   'Не важно'

        cons = update.message.text.strip()
        if cons == 'Не важно':
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text='Ну ок\n' + next_text(),
                                     reply_markup=min_cost_menu)
            return 2
        else:
            num = float(cons.split(' ')[-2])
            # print(num)
            if 'До' in cons:
                self.filtered_cars = list(filter(lambda x: x.consumption <= num, self.filtered_cars))
            else:
                self.filtered_cars = list(filter(lambda x: x.consumption > num, self.filtered_cars))
            # print(self.filtered_cars)
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text='А ты, я смотрю, шаришь\n' + next_text(),
                                     reply_markup=min_cost_menu)
            return 2

    def register_min_cost(self, update, context):
        def next_text():
            return "💵💵 Дальше - еще лучше, максимальная цена:\n" \
                   '1. до 1 млн. р\n' \
                   '2. до 1,5 млн. р\n' \
                   '3. до 2 млн. р\n' \
                   '4. до 3 млн. р\n' \
                   '5. до 4 млн. р\n' \
                   '6. Не важно\n'

        if 'р' in update.message.text:
            min_cost = float(update.message.text.split(' ')[1])
            self.filtered_cars = list(filter(lambda x: x.cost >= min_cost * 1000000, self.filtered_cars))
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="Учел\n" + next_text(),
                                     reply_markup=max_cost_menu)
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="Ладушки\n" + next_text(),
                                     reply_markup=max_cost_menu)
        return 3

    def register_max_cost(self, update, context):
        if 'р' in update.message.text:
            max_cost = float(update.message.text.split(' ')[1])
            self.filtered_cars = list(filter(lambda x: x.cost <= max_cost * 1000000, self.filtered_cars))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='🔎 Окей, я собрал достаточно информации, чтобы понять, что может подойти именно '
                                      'тебе, смотри:')
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=self.get_results(),
                                 reply_markup=main_menu,
                                 parse_mode=telegram.ParseMode.HTML)
        return ConversationHandler.END

    def get_results(self):
        final_text = [
            f'🚗 <b>{car.manufacturer} {car.model}</b>:\n•Расход на 100 км (л): {car.consumption}\n•Цена: {car.cost}\n' +
            f'•Корпус: {car.carcass}' for car in self.filtered_cars]
        self.filtered_cars = self.cars
        if final_text:
            return '\n'.join(final_text)
        else:
            return '😞 К сожалению, машин с заданными параметрами нет у нас в базе данных, попробуйте найти другую машину'

    def cancel(self, upd, context):
        self.filtered_cars = self.cars
        context.bot.send_message(chat_id=upd.message.chat_id,
                                 text="Как скажешь, начальник",
                                 reply_markup=main_menu)
        return ConversationHandler.END

    def restart_program(self):
        """Restarts the current program, with file objects and descriptors
           cleanup
        """
        print("Restarted")
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def main(self):
        self.updater.start_polling()
