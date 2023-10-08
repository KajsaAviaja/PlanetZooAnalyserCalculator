import json
from bs4 import BeautifulSoup
import re



dict = {}
f = open("data/List_of_Animals.html", "r", encoding="utf-8")
page = f.read()
f.close()



soup = BeautifulSoup(page, "html.parser")
animal_list = soup.find("table", class_="listofanimals").find("tbody").find_all("tr")

def analyseAnimal(a):
    td_list = a.find_all("td")
    if len(td_list) > 0:
        name = td_list[0].find("a").text
        try:
            conservation = td_list[1].find("a").find("img", alt=True)["alt"]
      
            type = "Habitat" if (td_list[2].text.strip() == "Full") else "Exhibit"
          
            dict[name] = {
                "Gameplay": {
                    "Type": type,
                    "Content pack": td_list[3].text.strip(),
                },
                "Origin": { 
                    "Conservation status": conservation,
                },
                "Habitat": {}              
            }
        
            content = GetAnimalContent(name)
            setOrigin(name, content)

            if type == "Habitat":
                analyseHabitatAnimal(name, content)
        except:
            pass

def setOrigin(name, content):
    try:
        dict[name]["Origin"]["Continent"] = content.find("h3", string="Continents").parent.find("div").text
    except:
        dict[name]["Origin"]["Continent"] = None
        #print("could not get continent for " + name)

    try:
        dict[name]["Origin"]["regions"] = re.split(
                ": |, ", content.find("h3", string="Regions").parent.find("div").text
                )   

    except:
        dict[name]["Origin"]["regions"] = []
        #print("could not get region for " + name)

def analyseHabitatAnimal(name, content):
    setFenceSpec(name, content)

def setFenceSpec(name, content):
    fence = content.find("h3", string="Fence Grade").parent.parent.find("div").text.replace(">", "").replace("(", "").replace(")", "").replace("m", "").replace("Grade", "").split(" ")
    print("helloooo" + fence)
    print("hello " + fence)
    grade_str = fence[0]
    if len(fence) == 2:
        height_str = fence[1]
        climbproof = False
    
    elif len(fence) == 4:
        height_str = fence[3]
        climbproof = True

    grade = float(grade_str)
    height = float(height_str)

    print("grade: "+ grade)
    dict[name]["Habitat"] = {"Fence": {"Grade": grade,"Height": height, "ClimbProof": climbproof,}}
    print("hello again")
  
        
 
    
            
def GetAnimalContent(name):

    
    f = open("data/animals/Red-Crowned_Crane.html", "r", encoding="utf-8")
    p = f.read()
    f.close()

    content = BeautifulSoup(p, "html.parser")
    
    return content
    

for i in range(1,20):
    analyseAnimal(animal_list[i])

#analyseAnimal(animal_list[1])
with open("data.json", "w") as outfile:
    outfile.write(json.dumps(dict, indent=4))


