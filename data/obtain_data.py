import requests
import pandas as pd

constellations = [
    "Andromeda", "Antlia", "Apus", "Aquarius", "Aquila", "Ara", "Aries", "Auriga", 
    "Boötes", "Caelum", "Camelopardalis", "Cancer", "Canes Venatici", "Canis Major", 
    "Canis Minor", "Capricornus", "Carina", "Cassiopeia", "Centaurus", "Cepheus", 
    "Cetus", "Chamaeleon", "Circinus", "Columba", "Coma Berenices", "Corona Australis", 
    "Corona Borealis", "Corvus", "Crater", "Crux", "Cygnus", "Delphinus", "Dorado", 
    "Draco", "Equuleus", "Eridanus", "Fornax", "Gemini", "Grus", "Hercules", 
    "Horologium", "Hydra", "Hydrus", "Indus", "Lacerta", "Leo", "Leo Minor", "Lepus", 
    "Libra", "Lupus", "Lynx", "Lyra", "Mensa", "Microscopium", "Monoceros", "Musca", 
    "Norma", "Octans", "Ophiuchus", "Orion", "Pavo", "Pegasus", "Perseus", "Phoenix", 
    "Pictor", "Pisces", "Piscis Austrinus", "Puppis", "Pyxis", "Reticulum", "Sagitta", 
    "Sagittarius", "Scorpius", "Sculptor", "Scutum", "Serpens", "Sextans", "Taurus", 
    "Telescopium", "Triangulum", "Triangulum Australe", "Tucana", "Ursa Major", "Ursa Minor", 
    "Vela", "Virgo", "Volans", "Vulpecula"
]

def fetch_stars(api_key, constellation):
    base_url = 'https://api.api-ninjas.com/v1/stars'
    results = []
    offset = 0
    while True:
        params = {
            'constellation': constellation,
            'offset': offset
        }
        headers = {'X-Api-Key': api_key}
        response = requests.get(base_url, headers=headers, params=params)
        data = response.json()
        if not data:
            break
        results.extend(data)
        offset += 30
    return results

def save_data(stars_data):
    df = pd.DataFrame(stars_data)
    df.to_csv('stars_data.csv', mode='a', header=False)  

api_key = 'PewrA/MGCHxgJ7ncmaC0Tw==2xzQLCjmoMvC6alK' # will be removed after project submission
all_stars = []
for constellation in constellations:
    stars_data = fetch_stars(api_key, constellation)
    save_data(stars_data)
    all_stars.extend(stars_data)  

print("All star data collected and saved.")
