from grab import Grab
from bs4 import BeautifulSoup
from datetime import datetime
import telebot, threading, time

ALERT_TIME = '19'

g = Grab(log_file='out.html')

user_data = []
with open('db.txt', 'r') as reader:
    user_data = reader.readlines()
user_data[0] = user_data[0].rstrip('\n')

now = datetime.now()
curr_time = now.strftime("%H")


def ShowStatistics():
    try:
        g.setup(post={"user": f"{user_data[0]}", "passwd": f"{user_data[1]}"})
        g.go('https://balakleya.skystat.com/index.cgi')
    except:
        time.sleep(1)
        print("Error ocurred")
        g.setup(post={"user": f"{user_data[0]}", "passwd": f"{user_data[1]}"})
        g.go('https://balakleya.skystat.com/index.cgi')


    f = open('out.html', "r")
    text = f.read()
    soup = BeautifulSoup(text, 'html.parser')
    my_dep = soup.find("tr", {"class": "odd"})
    dep_ch = my_dep.findChildren("td", recursive=False)
    days = soup.find("div", {'id': 'dv_user_info'})
    d_ch = days.findChildren("h3", recursive=False)

    resstr = ""
    for tag in dep_ch:
        resstr += tag.get_text()
    resstr += "\n"
    for tag in d_ch:
        resstr += tag.get_text()
    return resstr

bot = telebot.TeleBot('1650821709:AAF0OrGdGAjjRvERGUCFu7ByarMAliOX7w8')
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')
@bot.message_handler(commands=['chtime'])
def change_alert_time():
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.from_user.id == 266536993:
            ALERT_TIME = message
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.from_user.id == 266536993:
        if message.text.lower() == 'привет':
            bot.send_message(message.from_user.id, 'Привет!')
        elif message.text.lower() == 'инфа':
            bot.send_message(message.from_user.id, ShowStatistics())
        else:
            bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')
my_timer = None
def SendStat():
    bot.send_message(266536993, ShowStatistics())
def make_thr():
    global my_timer
    my_timer = threading.Timer(3700, make_thr)
    my_timer.start()
    SendStat()
if curr_time == ALERT_TIME:
    make_thr()
bot.polling(none_stop=True)