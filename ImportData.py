from bs4 import BeautifulSoup
import requests
import json

URL = "https://planetzoo.fandom.com/wiki/List_of_Animals"
response = requests.get(URL)

with open("data/List_of_Animals.html", "w", encoding="utf-8") as outfile:
    outfile.write(response.text)

soup = BeautifulSoup(response.text, "html.parser")
animal_list = soup.find("table", class_="listofanimals").find("tbody").find_all("tr")

for a in animal_list:
    td_list = a.find_all("td")
    if len(td_list) > 0:
        name = td_list[0].find("a").text

        URL = "https://planetzoo.fandom.com/wiki/" + name.replace(" ", "_")
        page = requests.get(URL)
        
        with open("data/animals/"+ name.replace(" ", "_")+ ".html", "w", encoding="utf-8") as outfile:
            outfile.write(page.text)
