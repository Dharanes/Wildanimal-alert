# import requests

# r = requests.get('https://get.geojs.io')

# print(r)

# ip_request = requests.get('https://get.geojs.io/v1/ip.json')
# ipAdd = ip_request.json()['ip']


# print(ip_request,ipAdd)

# url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
# print(url)
# geo_request = requests.get(url)
# print(geo_request)

# geo_data = geo_request.json()
# print(geo_data['city'])
# print(geo_data['region'])
import requests

class Location:
    def __init__(self):
        self.r = requests.get('https://get.geojs.io')

        self.ip_request = requests.get('https://get.geojs.io/v1/ip.json')
        self.ipAdd = self.ip_request.json()['ip']

        self.url = 'https://get.geojs.io/v1/ip/geo/' + self.ipAdd + '.json'
        self.geo_request = requests.get(self.url)

        self.geo_data = self.geo_request.json()        