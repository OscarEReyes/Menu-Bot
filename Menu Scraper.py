from bs4 import BeautifulSoup as BS4
import requests
import smtplib
from email.mime.text import MIMEText
import time


def find_number_of_meals(day):
    if day == 'Saturday' or 'Sunday':
        return 2
    else:
        return 3


def scrape_decider(number_of_meals, date):
    if number_of_meals == 2:
        brunch_menu = scrape_menu(1522, date)
        dinner_menu = scrape_menu(1524, date)
        create_weekend_text_file(brunch_menu, dinner_menu)
    else:
        breakfast = scrape_menu(1521, date)
        lunch = scrape_menu(1523, date)
        dinner = scrape_menu(1524, date)
        create_week_text_file(breakfast, lunch, dinner)


def scrape_menu(meal_id, date):
    meal_id = str(meal_id)
    menu_dict = {}
    food_list = []
    url = 'https://tamuk.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=6532&PeriodId=' + meal_id + '&MenuDate' \
          + date
    res = requests.get(url)
    res.raise_for_status()

    soup = BS4(res.text, 'html.parser')

    for group in soup.select('.menu-details-station'):
        category = group.find('h2').text
        food_items = group.select('.menu-details-station-item .menu-name a')
        for item in food_items:
            food_list.append(item.text)
        copy_list = food_list[:]
        menu_dict[category] = copy_list
    return menu_dict


def create_weekend_text_file(brunch_menu, dinner_menu):
    with open('menu.text', 'w') as f:
        write_to_text(f, "Brunch", brunch_menu.items())
        write_to_text(f, "Dinner", dinner_menu.items())


def create_week_text_file(breakfast, lunch, dinner):
    text_file = open('menu.text', 'w')
    write_to_text(text_file, "Breakfast", breakfast.items())
    write_to_text(text_file, "Lunch", lunch.items())
    write_to_text(text_file, "Dinner", dinner.items())
    text_file.close()


def write_to_text(text_file, meal, food_list):
    text_file.write(meal + "\n\n")
    for category, food in food_list.items():
        text_file.write(category + '\n')
        for food_item in food:
            text_file.write('\t' + food_item + '\n')


def create_message():
    with open('menu.text') as fp:
        msg = MIMEText(fp.read())
    return msg


def input_email():
    while True:
        email = input("What is your email?")
        if len(email.split()) == 1:
            if email[len(email):len(email) - 4:-1] == "moc." and "@" in email:
                return email


def authenticate_receiver():
    valid_answers = [
        'yes',
        'y'
    ]
    receiver = input("Are you 'o.scar_R@yahoo.com.mx'?")
    if receiver.lower()[0] in valid_answers:
        return 'o.scar_R@yahoo.com.mx'
    else:
        return input_email()


def send_email(msg):
    sender = 'tamukmenubot@yahoo.com'
    receiver = authenticate_receiver()
    msg['Subject'] = 'This is the menu for today: '
    msg['From'] = sender
    msg['To'] = receiver
    conn = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    conn.ehlo()
    conn.starttls()
    conn.login('tamukmenubot@yahoo.com', 'tamukmenurobot')
    conn.send_message(msg)
    conn.quit()


date = time.strftime("%Y-%m-%d")
day = time.strftime("%A")
number_of_meals = find_number_of_meals(day)
scrape_decider(number_of_meals, date)
msg = create_message()
send_email(msg)
