import json
import re
import requests
from bs4 import BeautifulSoup


dict = {}


URL = "https://planetzoo.fandom.com/wiki/List_of_Animals"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")


animal_list = soup.find("table", class_="listofanimals").find("tbody").find_all("tr")


def analyseAnimal(a):
    td_list = a.find_all("td")
    if len(td_list) > 0:
        name = td_list[0].find("a").text
        conservation = td_list[1].find("a").find("img", alt=True)["alt"]

        URL = "https://planetzoo.fandom.com/wiki/" + name.replace(" ", "_")
        page = requests.get(URL)

        content = BeautifulSoup(page.content, "html.parser").find("div", id="content")

        continent = content.find("h3", string="Continents").parent.find("div").text

        regions = re.split(
            ": |, ", content.find("h3", string="Regions").parent.find("div").text
        )

        (grade, height, climbproof) = getFenceSpec(content)

        dict[name] = {
            "conservation status": conservation,
            "type": "Habitat" if (td_list[2].text.strip() == "Full") else "Exhibit",
            "content pack": td_list[3].text.strip(),
            "continent": continent,
            "regions": regions,
            "fence": {
                "grade": int(grade),
                "height": int(height),
                "climbproof": climbproof,
            },
        }


def getFenceSpec(content):
    fence = (
        content.find("h3", string="Fence Grade")
        .parent.parent.find("div")
        .text.split(" ")
    )

    if len(fence) == 2:
        return (fence[0], fence[1].replace(">", "").replace("m", ""), False)
    elif len(fence) == 4:
        return (
            fence[0],
            fence[3]
            .replace(">", "")
            .replace("(", "")
            .replace(")", "")
            .replace("m", ""),
            True,
        )
    else:
        return (None, None, None)


analyseAnimal(animal_list[a])


print(json.dumps(dict, indent=4))
