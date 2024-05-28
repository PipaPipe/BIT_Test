import time
import certifi
import ssl
import json

import geopy.geocoders
from geopy.geocoders import Nominatim
import geopandas as gpd
from shapely.geometry import Point

# надстройка контекста для библиотеки geopy
# в старых версиях windows и на макбуках с arm процессорами возникает
# проблема с подтверждением ssl сертификации, поэтому приходится использовать незащищенный протокол http
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx


# Вспомогательная функция для вывода успешности операции
def print_success_or_not(val):
    if val:
        print("\nУспешно!\n")
        time.sleep(2)
        return
    print("\nПопробуйте еще раз!\n")
    time.sleep(2)
    return


# Получение объекта location исходя из улицы и города
def get_location(city, street):
    geolocator = Nominatim(user_agent='Test', scheme='http')
    location = geolocator.geocode(city + " " + street)
    return location


# Преобразование объекта location в координаты
def get_coordinates(location):
    lat = location.raw['lat']
    lon = location.raw['lon']
    return lat, lon


# Преобразование датафрейма в geojson файл
def df_to_geojson(df):
    gdf = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df['lat'], df['lon'])])
    geojson_str = gdf.to_json()
    with open('./Reports/geoJSON.json', 'w') as f:
        json.dump(geojson_str, f)
