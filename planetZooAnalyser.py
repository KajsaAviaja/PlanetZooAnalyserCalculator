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
        try:
            conservation = td_list[1].find("a").find("img", alt=True)["alt"]

            URL = "https://planetzoo.fandom.com/wiki/" + name.replace(" ", "_")
            page = requests.get(URL)

            try:
                content = BeautifulSoup(page.content, "html.parser").find("div", id="content")
            except:
                raise Exception("could not find content")
            
            try:
                continent = content.find("h3", string="Continents").parent.find("div").text
            except:
                raise Exception("could not find continent")
            
            try:
                regions = re.split(
                    ": |, ", content.find("h3", string="Regions").parent.find("div").text
                )   
            except:
                regions = []

            try:
                type = "Habitat" if (td_list[2].text.strip() == "Full") else "Exhibit"
            except:
                raise Exception("could not find type")
            dict[name] = {
                "conservation status": conservation,
                "type": type,
                "content pack": td_list[3].text.strip(),
                "continent": continent,
                "regions": regions,
            }

            if(type == "Habitat"):
                analyseHabitatAnimal(dict[name],content)
            else:
                analyseExhibitAnimal(dict[name],content)
        
        except Exception as e:
            print("error in " + name + ": " + str(e))
    

def analyseHabitatAnimal(dict, content):
    dict["fence"] = getFenceSpec(content)
    

def analyseExhibitAnimal(dict, content):
    pass

def getFenceSpec(content):

    try:
        fence = (
            content.find("h3", string="Fence Grade")
            .parent.parent.find("div")
            .text.replace(">", "").replace("(", "").replace(")", "").replace("m", "").replace("Grade", "").split(" ")
        )
    except: 
        fence = ["-1","-1"]
        raise Exception("Could not find fence specs")
        
 
    grade_str = fence[0]
    height_str = "-1"
    climbproof = False


    if len(fence) == 2:
        height_str = fence[1]
        
    elif len(fence) == 4:
            height_str = fence[3]
            climbproof = True,
        

    grade = float(grade_str)
    height = float(height_str)

    return {"grade": grade,"height": height, "climbproof": climbproof,}
    
            

for i in range(50,100):
    analyseAnimal(animal_list[i])


#print(json.dumps(dict, indent=4))
