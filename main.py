import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd
import time
import datetime

start_time = time.time()


def scrap_google():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
    }

    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    search = []
    header = []

    query = input("Поиск: ")
    query = query.replace(' ', '')

    try:
        url = f"https://scholar.google.com/scholar?q={query}"
        r = requests.get(url=url, headers=headers)
        src = r.text

        with open("index.html", "w", encoding="utf-8") as file:
            file.write(src)

        with open("index.html", encoding="utf-8") as file:
            site = file.read()

        soup = BeautifulSoup(site, "lxml")
        pages = soup.find_all("div", class_="gs_r gs_or gs_scl")
        for item in pages:
            url_item = item.find("a").get("href") # вдруг вам понадобится url

            title = item.find("div", class_="gs_ri").find('h3', class_='gs_rt').find("a").text

            source = item.find('div', class_='gs_a').text

            r = item.find("div", class_="gs_ri").find('div', class_='gs_fl')
            try:
                number_of_citations = r.find_all("a")
                noc = number_of_citations[2].text.split(":")[1].strip()
            except Exception as _ex:
                noc = None

            search.append([title, source, noc])

        header = (['title', 'source', 'number_of_citations'])

        df = pd.DataFrame(search, columns=header)
        df.to_csv("work.csv", sep=";", encoding="utf-8-sig")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    scrap_google()
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")