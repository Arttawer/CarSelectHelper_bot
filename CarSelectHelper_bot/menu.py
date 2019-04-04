from telegram import KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup([[KeyboardButton(text='/start')],
                                 [KeyboardButton(text='Найти машину')]])

carcass_menu = ReplyKeyboardMarkup([
    [KeyboardButton(text='Седан'), KeyboardButton(text='Купэ')],
    [KeyboardButton(text='Универсал'), KeyboardButton(text='Внедорожник')],
    [KeyboardButton(text='Хэтчбек'), KeyboardButton(text='Кабриолет')],
    [KeyboardButton(text='Минивэн'), KeyboardButton(text='Не важно')],
    [KeyboardButton(text='/cancel')]
])

consumption_menu = ReplyKeyboardMarkup([
    [KeyboardButton(text='До 8 л'), KeyboardButton(text='До 10 л')],
    [KeyboardButton(text='До 13 л'), KeyboardButton(text='До 15 л')],
    [KeyboardButton(text='Больше 15 л'), KeyboardButton(text='Не важно')],
    [KeyboardButton(text='/cancel')]
])

min_cost_menu = ReplyKeyboardMarkup([
    [KeyboardButton(text='От 0.8 млн р.'), KeyboardButton(text='От 1 млн р.')],
    [KeyboardButton(text='От 1.5 млн р.'), KeyboardButton(text='От 2 млн р.')],
    [KeyboardButton(text='От 3 млн р.'), KeyboardButton(text='От 3 млн р.')],
    [KeyboardButton(text="Не важно")],
    [KeyboardButton(text='/cancel')]
])

max_cost_menu = ReplyKeyboardMarkup([
    [KeyboardButton(text='до 1 млн р.'), KeyboardButton(text='до 1.5 млн р.')],
    [KeyboardButton(text='до 2 млн р.'), KeyboardButton(text='до 3 млн р.')],
    [KeyboardButton(text='до 4 млн р.'), KeyboardButton(text='Не важно')],
    [KeyboardButton(text='/cancel')]
])
