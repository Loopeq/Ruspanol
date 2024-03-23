import requests
from bs4 import BeautifulSoup


from data.database import insert_sections, insert_words

URL = "https://espanol.online/lexic/by_theme?language=ru&ysclid=lu2iuwl64b31496901"
BASE_URL = "https://espanol.online/"


def get_sections():
    req = requests.get(URL)
    soup = BeautifulSoup(req.text, "lxml")
    sections = soup.find("div", class_="row lexic_row").find_all("div", "col-12")
    sections_list = []
    for section in sections:
        title = section.find("h3")
        level = section.find("div", class_="level")
        id = section.find("a", class_="shadowbox", href=True)["href"]
        sections_list.append({"id": id, "title" : title.text.capitalize(), "level": level.text})
    return sections_list

def get_words(section_id: str, db_id: int):
    current_url = BASE_URL + section_id
    req = requests.get(current_url)
    soup = BeautifulSoup(req.text, "lxml")
    words = soup.find_all("div", class_="lex_row")
    words_list = []
    for word in words:
       rus, es = word.find('div', class_="lex_col col-ru"), word.find('div', class_="lex_col col-es")
       words_list.append((rus.text, es.text, db_id))
    return words_list

def main():
    sections = get_sections()
    for ind in range(len(sections)):
        insert_sections(sections[ind])
        words = get_words(sections[ind]["id"], ind+1)
        insert_words(words)

if __name__ == "__main__":
    main()