"""
Date: 13 Februari 2022
Time: 17:12:16 WIB
Magnitude: 5.0
Depth: 10 km
Location:
    Lat=5.94 LU - Long=125.59 BT
Center: 247 km BaratLaut MELONGUANE-SULUT
Descripition: tidak berpotensi TSUNAMI
"""
import requests
from bs4 import BeautifulSoup


def data_extraction():
    try:
        content = requests.get('https://www.bmkg.go.id')
    except Exception:
        return None
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        title = soup.find('title')
        print(title.string)

        time = soup.find('span', {'class': 'waktu'})
        date = time.text.split(', ')[0]
        time = time.text.split(', ')[1]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        n = 0
        magnitude = None
        depth = None
        lat = None
        long = None
        center = None
        desc = None

        for i in result:
            #print(n, i)
            if n == 1:
                magnitude = i.text
            elif n ==2:
                depth = i.text
            elif n ==3:
                coordinate = i.text.split(' - ')
                lat = coordinate[0]
                long = coordinate[1]
            elif n == 4:
                center = i.text
            elif n == 5:
                desc = i.text
            n = n+1




        result_data = dict()
        result_data['date'] = date
        result_data['time'] = time
        result_data['mag'] = magnitude
        result_data['depth'] = depth
        result_data['coordinate'] = {
            'lat': lat, 'long': long
        }
        result_data['center'] = center
        result_data['desc'] = desc

        return result_data
    else:
        return None

def show_data(result):
    if result is None:
        print('Cannot find the data')
        return
    print('Source: https://www.BMKG.co.id')
    print(f'Date: {result["date"]}')
    print(f'Time: {result["time"]}')
    print(f'Magnitude: {result["mag"]}')
    print(f'Depth: {result["depth"]}')
    print(f'Coordinate: lat={result["coordinate"]["lat"]} long={result["coordinate"]["long"]}')
    print(f'Center: {result["center"]}')
    print(f'Description: {result["desc"]}')


if __name__ == '__main__':
    print('Latest Earthquake Detection App')
    result = data_extraction()
    show_data(result)
