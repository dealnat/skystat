from grab import Grab
from bs4 import BeautifulSoup
import telebot,  threading
import schedule, sqlite3


g = Grab(log_file='bill_out.html') #creating grab obj and say where to save page
def get_stat(auth_log, auth_pass):
    g.go('https://bill.univ.kiev.ua/index.php?act_id=access',post={"login": f"{auth_log}" , "password": f"{auth_pass}"}) #go to the mainpage

    f = open('bill_out.html', "r", encoding="cp1251")
    text = f.read()
    soup = BeautifulSoup(text, 'html.parser')
    font_params =  soup.find_all('font')
    balance = font_params[1].text
    f.close()

    return balance
print(get_stat("host2063ok", '1234567'))