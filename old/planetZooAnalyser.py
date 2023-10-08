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
            
            addLocation(content)

            try:
                type = "Habitat" if (td_list[2].text.strip() == "Full") else "Exhibit"
            except:
                raise Exception("could not find type")
            dict[name] = {
                "conservation status": conservation,
                "type": type,
                "content pack": td_list[3].text.strip(),
               
            }

            #addLocation(dict[name],content)

            """ if(type == "Habitat"):
                analyseHabitatAnimal(dict[name],content)
            else:
                analyseExhibitAnimal(dict[name],content) """
        
        except Exception as e:
            print("error in " + name + ": " + str(e))

def addLocation(dict, content):
    try:
        dict["continent"] = content.find("h3", string="Continents").parent.find("div").text
    except:
        dict["continent"] = None
            
    try:
        regions = re.split(
                    ": |, ", content.find("h3", string="Regions").parent.find("div").text
                )   
    except:
        regions = []
    return continent,regions
    

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
    
            

for a in animal_list:
    analyseAnimal(a)


#print(json.dumps(dict, indent=4))

with open("data.json", "w") as outfile:
    outfile.write(json.dumps(dict, indent=4))