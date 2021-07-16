import requests
from bs4 import BeautifulSoup
import unicodedata
import telegram
from datetime import date
from emoji import emojize
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--meal", required=True, help="Specify one of ['breakfast', 'lunch', 'dinner']"
)

args = parser.parse_args()


with open("token.txt", "r") as f:
    token = f.readline()

emo = lambda x: emojize(f":{x}:", use_aliases=True)
ending = f"‾͟͟͞((({emo('fork_and_knife')}ˋ⁻̫ˊ)—̳͟͞͞{emo('fork_and_knife')}               {emo('meat_on_bone')}"


def get_menu(date: date, meal: str) -> list:
    url = f"https://snuco.snu.ac.kr/ko/foodmenu?field_menu_date_value_1%5Bvalue%5D%5Bdate%5D=&field_menu_date_value%5Bvalue%5D%5Bdate%5D={today.month}%2F{today.day}%2F{today.year}"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    # Get the list of restaurant names
    restaurant = soup.select(
        "#main-content > div.contentsArea > div > div > div.view-content > table > tbody > tr > td.views-field.views-field-field-restaurant"
    )
    restaurant = [rest.get_text().strip().split("(")[0] for rest in restaurant]

    # Get menus
    menu = soup.select(
        f"#main-content > div.contentsArea > div > div > div.view-content > table > tbody > tr > td.views-field.views-field-field-{meal}"
    )
    menu = [unicodedata.normalize("NFKD", l.get_text().strip()) for l in menu]

    return tuple(zip(restaurant, menu))


def send_menu(chat_id: str, date: date, interest: list, meal: str) -> None:

    bot = telegram.Bot(token=token)
    final = [data for data in get_menu(date=date, meal=meal) if data[0] in interest]
    date_text = today.strftime(format="%Y년 %m월 %d일")

    bot.send_message(
        chat_id=chat_id,
        text=f"{emo('egg')} {date_text} | {meal.upper()} {emo('rice')}",
        parse_mode="Markdown",
    )

    for menu in final:
        text = f"#*{menu[0]}*\nㅡ\n{menu[1]}"
        bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
    bot.send_message(
        chat_id=chat_id,
        text=ending,
        parse_mode="Markdown",
    )
    return date_text


# f"{emo('house_with_garden')}{emo('fork_and_knife')}          {emo('running')}{emo('runner')}{emo('dash')}"

if __name__ == "__main__":
    today = date.today()
    interest = ("학생회관식당", "3식당", "두레미담")
    meal = args.meal
    chat_id = "@snumenu"

    success = send_menu(chat_id=chat_id, date=today, interest=interest, meal=meal)
    print(f"{success} - Message was sent!")
