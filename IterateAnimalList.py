import json
import re
from bs4 import BeautifulSoup

dict = {}
f = open("data/List_of_Animals.html", "r", encoding="utf-8")
page = f.read()
f.close()


soup = BeautifulSoup(page, "html.parser")
animal_list = soup.find("table", class_="listofanimals").find("tbody").find_all("tr")


def analyseAnimal(a):
    td_list = a.find_all("td")
    name = td_list[0].find("a").text
    print(name)
    conservation = td_list[1].find("a").find("img", alt=True)["alt"]
    type = "Habitat" if (td_list[2].text.strip() == "Full") else "Exhibit"
    edition = td_list[3].text.strip()

    with open(
        "data/animals/" + name.replace(" ", "_") + ".html", "r", encoding="utf-8"
    ) as file:
        content = BeautifulSoup(file.read(), "html.parser")

    continent = content.find("h3", string="Continents").parent.find("div").text

    regions = (
        re.split(": |, ", content.find("h3", string="Regions").parent.find("div").text)
        if content.find("h3", string="Regions") is not None
        else []
    )
    if type == "Habitat":
        fence = (
            (
                content.find("h3", string="Fence Grade")
                .parent.parent.find("div")
                .text.replace(">", "")
                .replace("(", "")
                .replace(")", "")
                .replace("m", "")
                .replace("Grade", "")
                .split(" ")
            )
            if content.find("h3", string="Fence Grade") is not None
            else [-1, -1]
        )
        fence = [f for f in fence if f != ""]
        climbproof = False
        grade_str = fence[0]
        height_str = -1
        if len(fence) == 2:
            height_str = fence[1]
            climbproof = False

        elif len(fence) == 4:
            height_str = fence[3]
            climbproof = True

        grade = float(grade_str) if grade_str != "" else -1
        height = float(height_str)

        [land, water] = content.find("h3", string="Land Area").parent.parent.find_all(
            "div"
        )
        [climbing, temperature] = (
            content.find("h3", string="Climbing Area").parent.parent.find_all("div")
            if content.find("h3", string="Climbing Area") is not None
            else [None, None]
        )

        req = [
            [
                float(f) if f != "" else 0.0
                for f in (
                    r.text.replace("m²", "")
                    .replace(" /ea. add'l", "")
                    .replace(" +", "")
                    .split(" ")
                )
            ]
            if r is not None
            else [[-1, -1], [-1, -1], [-1, -1]]
            for r in [land, water, climbing]
        ]

        temp = (
            temperature.text.replace("℃", "").replace(" ", "").split("‒")
            if temperature is not None
            else [-1, -1]
        )

        if len(temp) == 3:
            temp.pop(0)
            temp[0] = "-" + temp[0]
        if len(temp) == 4:
            temp.pop(1)
            temp[1] = "-" + temp[1]
        temperature = tuple(temp)

        biome = content.find("h3", string="Biomes").parent.parent.find("img")["alt"]

        social = [
            i.text
            for i in content.find("h3", string="Group Size").parent.parent.find_all(
                "div"
            )
        ]
        male_b = tuple([float(i) for i in social[1].split("‒")])
        female_b = tuple([float(i) for i in social[2].split("‒")])
        group = re.findall("\d+", social[0])

        tax = [
            i.text for i in content.find("h2", string="Taxonomy").parent.find_all("div")
        ]

        compatible = [
            (i["title"])
            for i in content.find("th", class_="compatible-text").find_all("a")
            if i.has_attr("title")
        ]
        feeding = [
            i.text
            for i in content.find("big", string="FEEDING STATIONS").parent.find_all("a")
        ]

        e_food = [
            i.text
            for i in content.find("big", string="FOOD ENRICHMENT").parent.find_all("a")
        ]
        e_hab = [
            i.text
            for i in content.find("big", string="HABITAT ENRICHMENT").parent.find_all(
                "a"
            )
        ]

        dict[name] = {
            "Gameplay": {"Type": type, "Edition": edition},
            "Origins": {
                "Continent": continent,
                "Regions": regions,
                "IUCN Status": conservation,
            },
            "Habitat": {
                "Fence": {"Grade": grade, "Height": height, "Climb Proof": climbproof},
                "Requirements": {
                    "Land": {"Base": req[0][0], "Extra": req[0][1]},
                    "Water": {"Base": req[1][0], "Extra": req[1][1]},
                    "Climbing": {"Base": req[2][0], "Extra": req[2][1]},
                },
                "Temperature": temperature,
                "Biome": biome,
            },
            "Group Size": {
                "Mixed": {
                    "Size": (group[0], group[1]),
                    "Female": group[3] if (len(group) > 3) else group[1],
                    "Male": group[2] if (len(group) > 3) else group[1],
                },
                "Female": female_b,
                "Male": male_b,
            },
            "Taxonomy": {
                "Class": tax[0],
                "Order": tax[1],
                "Family": tax[2],
                "Genus": tax[3],
            },
            "Preference": {
                "Food": feeding,
                "Enrichment": {"Food": e_food, "Habitat": e_hab},
            },
            "Compatible Animals": compatible,
        }
    else:
        dict[name] = {
            "Gameplay": {"Type": type, "Edition": edition},
            "Origins": {
                "Continent": continent,
                "Regions": regions,
                "IUCN Status": conservation,
            },
        }


for i in range(1, 171):
    analyseAnimal(animal_list[i])


with open("data.json", "w") as outfile:
    outfile.write(json.dumps(dict, indent=4))
