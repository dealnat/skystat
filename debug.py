from grab import Grab
from bs4 import BeautifulSoup
import telebot, time, threading
import schedule

bot = telebot.TeleBot('1650821709:AAF0OrGdGAjjRvERGUCFu7ByarMAliOX7w8')
#bot = telebot.TeleBot('1830250329:AAGEG6Atuq3g49ztoFHt9j9cDkqDc6R3YaI')
g = Grab(log_file='d_out.html') #creating grab obj and say where to save page



def send_stat():
    bot.send_message(266536993, get_stat())
def get_stat():
    g.setup(post={"user": "5687077894" , "passwd": "EP69cysrW3"} ) #addimg data to post-request
    g.go('https://balakleya.skystat.com/index.cgi') #go to the mainpage

    f = open('d_out.html', "r")
    text = f.read()
    soup = BeautifulSoup(text, 'html.parser')
    my_dep = soup.find("tr", {"class": "odd"})
    dep_ch = my_dep.findChildren("td", recursive=False)
    days = soup.find("div", {'id': 'dv_user_info'})
    d_ch = days.findChildren("h3", recursive=False)
    f.close()

    resstr = ""
    for tag in dep_ch:
        resstr += tag.get_text()
    resstr += "\n"
    for tag in d_ch:
        resstr += tag.get_text()

    print(resstr)
    return resstr
schedule.every().day.at("22:15").do(send_stat)
#schedule.every(1).minutes.do(send_stat)
def thread_pending():
    while True:
        schedule.run_pending()
thread = threading.Thread(target=thread_pending)
thread.start()
while 1:
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')




    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.from_user.id == 266536993:
            if message.text.lower() == 'инфа':
                bot.send_message(message.from_user.id, get_stat())

            else:
                bot.send_message(message.from_user.id, 'Invalid')


    @bot.message_handler(commands=['sos'])
    def wellcome(message):
        if message.chat.type == 'private':
            bot.send_message(message.chat.id, 'Hello')



    bot.polling()

