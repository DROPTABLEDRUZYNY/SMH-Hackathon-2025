import random
import json

titles = [
    "Telewizor porzucony w parku",
    "smieci pozostawione pod drzewem",
    "Fotel zalegajacy na chodniku",
    "Puste butelki w lesie",
    "Zniszczony rower w krzakach",
    "Stare opony w poblizu placu zabaw",
    "Wyrzucone kartony w centrum miasta",
    "Stol po imprezie w parku",
    "Opakowania po jedzeniu w parku miejskim",
    "Zlamana lawka na skwerze",
    "Niedopalki papierosow przy lawce",
    "Torba pelna smieci w zagajniku",
    "Wyrzucone ubrania na plazy",
    "Zniszczony fotel na polanie",
    "Zimowe rekawiczki porzucone w parku",
    "Stare gazety zostawione na chodniku",
    "Plastikowa butelka w rzece",
    "Popielniczka pelna smieci w parku",
    "Wyrzucone pudelka na chodniku",
    "Zatrzymany pojazd w poblizu drzew",
    "Pojemniki po napojach w poblizu przystanku",
    "Zlamana deska w parku",
    "Wyrzucone zabawki wsrod drzew",
    "Wyrzucone jedzenie na trawie",
    "Zbutwiale drewno w lesie",
    "Zniszczona kanapa na ulicy",
    "Polamany parasol w parku",
    "Resztki jedzenia przy koszu",
    "Zawodowy sprzet w opuszczonym miejscu",
    "Plastikowa torba w stawie",
    "Wyrzucone kartony w zakatku",
    "Sluchawki porzucone przy drodze",
    "Telewizor bez ekranu na poboczu",
    "Siedzisko do fotela w krzakach",
    "Wyrzucone kapcie na trawie",
    "Zabawki dla dzieci porzucone w parku",
    "Otwarty karton w poblizu sklepu",
    "Stare papiery na ulicy",
    "Porzucony bagaz w okolicach stacji",
    "Wyrzucone akcesoria do sportow wodnych na plazy",
    "Zbutwiale krzeslo przy rzece",
    "Stare skrzynki na owoce w parku",
    "Wyrzucone opakowania po fast foodzie",
    "Wyrzucony namiot na polanie",
    "Puszki po napojach przy wejsciu do parku",
    "Pusty plecak w parku",
    "Wyrzucony sprzet RTV na ulicy",
    "Zrzut z roslinami w ogrodzie",
    "Stare ksiazki na krawezniku",
    "Zniszczony stol na rynku",
    "Wyrzucone torby z odpadkami w lesie",
    "Resztki materialow budowlanych w parku",
    "Szesc opakowan po kawie przy budce",
    "Zatrzymany motor na poboczu drogi",
    "Wyrzucone krzesla na trawie",
    "Tluste papierki po fast foodzie w parku",
    "Zniszczony fotel ogrodowy w parku",
    "Zupa w kartonie wsrod drzew",
    "Resztki drewna przy stawie",
    "Wyrzucone odziez na plazy",
    "Wyrzucony telefon na chodniku",
    "Zuzyte pilki w parku",
    "Niedopalone znicze na grobach",
    "Skorzana torba porzucona w parku",
    "Zbutwiala deska na smietniku",
    "Pudelka po pizzy na chodniku",
    "Resztki po grillu przy jeziorze",
    "Zamarzniety stol w parku",
    "Dzinsy pozostawione na ulicy",
    "Resztki po imprezie w parku",
    "Pusta skrzynka z narzedziami przy drodze",
    "Wyrzucony komputer w okolicy budowy",
    "Wyrzucone buty w parku",
    "Uzywane ubrania porzucone w poblizu drogi",
    "Stare plyty winylowe na skraju lasu",
    "Zuzyte sprzety w parku",
    "Wyrzucone opakowania po napojach w lesie",
    "Zlamany stol na rynku",
    "Zniszczona opona na chodniku",
    "Resztki po grillu na plazy"
]

LAT_MIN = 49.0 
LAT_MAX = 54.9
LON_MIN = 14.0
LON_MAX = 24.0

def generate_random_location(title):
    latitude = round(random.uniform(LAT_MIN, LAT_MAX), 5)
    longitude = round(random.uniform(LON_MIN, LON_MAX), 5)
    scale = random.choice([1, 2, 3])
    return {
        "name": title,
        "latitude": latitude,
        "longitude": longitude,
        "scale": scale
    }

generated_locations = [generate_random_location(title) for title in titles]

locations_json = json.dumps(generated_locations, indent=2)

with open("locations_data.json", "w") as f:
    f.write(locations_json)

print("Dane zostaly zapisane do pliku locations_data.json")
