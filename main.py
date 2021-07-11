from grab import Grab
from bs4 import BeautifulSoup
import telebot,  threading
import schedule, sqlite3

bot = telebot.TeleBot('1650821709:AAF0OrGdGAjjRvERGUCFu7ByarMAliOX7w8')
g = Grab(log_file='d_out.html') #creating grab obj and say where to save page


def get_cred():
    uid = 0
    auth_log = ""
    auth_pass = ""

    return [uid,auth_log, auth_pass]
def send_stat():
    con = sqlite3.connect('dbdir/users.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM userdata'):
        bot.send_message(row[0], get_stat(row[1],row[2]))
    con.close()
def get_stat(auth_log, auth_pass):
    g.setup(post={"user": f"{auth_log}" , "passwd": f"{auth_pass}"} ) #adding data to post-request
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
schedule.every().day.at("14:03").do(send_stat)
#schedule.every(1).minutes.do(send_stat)
def thread_pending():
    while True:
        schedule.run_pending()
thread = threading.Thread(target=thread_pending)
thread.start()

while 1:
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}, your id is {message.from_user.id}')


    @bot.message_handler(commands=['useradd'])
    def adduser(message):
        if message.from_user.id == 266536993:
            contr = sqlite3.connect('dbdir/users.db')
            curcon = contr.cursor()
            commandl = message.text.split()
            curcon.execute("INSERT INTO userdata VALUES(?, ?, ?)", (commandl[1], commandl[2], commandl[3]))
            contr.commit()
            for row in curcon.execute('SELECT * FROM userdata'):
                print(row)
            print("\n")
            bot.send_message(message.from_user.id, f"User added with this data VALUES({commandl[1]},\"{commandl[2]}\",\"{commandl[3]}\");")
        else:
            bot.send_message(message.from_user.id, "You are not allowed to execute this command")
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.from_user.id == 266536993:
            if message.text.lower() == 'инфа':
                bot.send_message(message.from_user.id, get_stat())

            else:
                bot.send_message(message.from_user.id, 'Invalid')
    bot.polling()
