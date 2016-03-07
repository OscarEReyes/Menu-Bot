from bs4 import BeautifulSoup as BS4
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime

def find_number_of_meals(day):
    if day == 'Saturday' or 'Sunday':
        return 2
    else: 
        return 3

def scrapeDecider(numberOfMeals,date): 
    if numberOfMeals == 2:
        brunch_menu = scrapeMenu(1522,date)
        dinner_menu = scrapeMenu(1524,date)
        createWeekendTextFile(brunch_menu, dinner_menu)
    else:
        breakfast = scrapeMenu(1521,date)
        lunch = scrapeMenu(1523,date)
        dinner = scrapeMenu(1524,date)
        createWeekTextFile(breakfast,lunch,dinner)
        
def scrapeMenu(x): 
    x = str(x)
    menu_dict={}
    foodList = []
    url = 'https://tamuk.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=6532'+'&PeriodId='+ x +'&MenuDate'+ date
    res = requests.get(url)
    res.raise_for_status()
    
    soup = BS4(res.text, 'html.parser')
    elems = soup.select('#RenderMenuDetailsSection')
    
    for group in soup.select('.menu-details-station'):  
        category = group.find('h2').text 
        food_items = group.select('.menu-details-station-item .menu-name a') 
        for item in food_items: 
            foodList.append(item.text)
        copy_list = foodList[:]
        menu_dict[category] = copy_list  
    return menu_dict

def createWeekendTextFile(brunch_menu,dinner_menu):
    text_file = open('menu.text','w')
    write_to_text(text_file, "Brunch", brunch_menu.items())
    write_to_text(text_file, "Dinner", dinner_menu.items())
    textfile.close()
    
def createWeekTextFile(breakfast,lunch,dinner):
    text_file = open('menu.text','w')
    write_to_text(text_file, "Breakfast", breakfast.items())   
    write_to_text(text_file, "Lunch", lunch.items())
    write_to_text(text_file, "Dinner", dinner.items())
    textfile.close()
    
def write_to_text(self,text_file,food_period,food_list):
    text_file.write(food_period + "\n\n")
    for category,food in food_list:
        text_file.write(category + '\n')
        for food_item in food:
            textfile.write('\t' + food_item + '\n')

def createMessage():
    with open('menu.text') as fp:
        msg = MIMEText(fp.read())
    return msg

def input_email():
    while True:
        email = input("What is your email?")
        if len(email.split()) == 1:
            if email[len(email):len(email)-4:-1] == "moc." and \
                "@" in email:
                    return email

def sendEmail(msg):
    sender = 'tamukmenubot@yahoo.com'
    reciver = input("Are you 'o.scar_R@yahoo.com.mx'?")
    if reciever.lower()[0] == "y":
        reciever ='o.scar_R@yahoo.com.mx' 
    else:
        reciever = input_email()
    msg['Subject'] = 'This is the menu for today: '
    msg['From'] = sender
    msg['To'] = reciever
    conn = smtplib.SMTP('smtp.mail.yahoo.com',587)
    conn.ehlo()
    conn.starttls()
    conn.login('tamukmenubot@yahoo.com', 'tamukmenurobot')
    conn.send_message(msg)
    conn.quit()

date = time.strftime("%Y-%m-%d")
day = time.strftime("%A")
number_of_meals = find_number_of_meals(day)
scrapeDecider(number_of_meals,date)
msg = createMessage()
sendEmail(msg)
