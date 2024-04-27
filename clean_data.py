import pandas as pd
import numpy as np

data = pd.read_csv('stars_data.csv')
print(data.isnull().sum())

def parse_right_ascension(ra):
    try:
        units = ra.replace('h', '').replace('m', '').replace('s', '').split()
        if len(units) == 3:
            hours, minutes, seconds = map(float, units)
            return hours + minutes/60 + seconds/3600
    except:
        return np.nan
    
def parse_declination(dec):
    if isinstance(dec, float):
      return dec
    try:
        dec = dec.strip().replace('\u2212', '-')  
        dec = dec.replace('°', ' ').replace('′', ' ').replace('″', ' ').replace('+', ' ').strip()
        sign = -1 if '-' in dec else 1
        dec = dec.replace('-', ' ').strip()  

        units = dec.split()
        if len(units) == 3:
            degrees, minutes, seconds = map(float, units)
            return sign * (degrees + minutes / 60 + seconds / 3600)
    except Exception as e:
        print(f"Error parsing declination: {dec} - {str(e)}")
        return np.nan

data['declination'] = data['declination'].apply(parse_declination)
data['right_ascension'] = data['right_ascension'].apply(parse_right_ascension)
data = data.dropna(subset=['apparent_magnitude', 'absolute_magnitude', 'distance_light_year', 'spectral_class'])


print(data.isnull().sum())

data.to_csv('cleaned_data.csv', index=False)
