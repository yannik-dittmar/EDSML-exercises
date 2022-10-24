import urllib.request, json
import os.path
import ssl
import shutil
import random
import codecs

CANTEENS_URL = 'https://openmensa.org/api/v2/canteens/'
CANTEENS_AMOUNT = 10
CANTEENS_FOLDER = './canteens'

def loadRandomCanteens():
    with urllib.request.urlopen(CANTEENS_URL) as url:
        data = json.load(url)
        random.shuffle(data)
        return data[:CANTEENS_AMOUNT]


def loadDaysFromCanteen(canteenId):
    with urllib.request.urlopen(f"{CANTEENS_URL}{canteenId}/days") as url:
        data = json.load(url)
        return map(lambda x: x['date'], data)

def loadMealsFromDay(canteenId, day):
    with urllib.request.urlopen(f"{CANTEENS_URL}{canteenId}/days/{day}/meals") as url:
        data = json.load(url)
        return data

def main():
    ssl._create_default_https_context = ssl._create_unverified_context

    if os.path.exists(CANTEENS_FOLDER):
        shutil.rmtree(CANTEENS_FOLDER)
    os.mkdir(CANTEENS_FOLDER)

    canteens = loadRandomCanteens()
    for canteen in canteens:
        with codecs.open(os.path.join(CANTEENS_FOLDER, f"[{canteen['id']}] {canteen['name'].replace('/', ',')}.txt"), 'w', 'utf-8') as file:
            print(f"{canteen['name']}")
            file.write(f"{canteen['name']}\n")
            days = loadDaysFromCanteen(canteen['id'])
            for day in days:
                print(f"  {day}")
                file.write(f"  {day}\n")
                meals = loadMealsFromDay(canteen['id'], day)
                for meal in meals:
                    print(f"    {meal['name']}")
                    file.write(f"    {meal['name']}\n")

if __name__ == '__main__':
    main()
