import requests


def must_respond(response: requests.Response) -> requests.Response:
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        quit(1)

    return response


class Map:
    STATIC_MAPS_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
    GEOCODER_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
    SEARCH_MAPS_KEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    MODES = ("landscape", "road", "admin")

    STATIC_MAP_SIZE = (600, 450)
    STATIC_MAP_FILE = "map.png"

    STATIC_MAPS_API_SERVER = "https://static-maps.yandex.ru/v1/"
    GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
    SEARCH_MAPS_API_SERVER = "https://search-maps.yandex.ru/v1/"

    DEGREES_IN_METER = 0.00001
    
    def __init__(self):
        self.is_dark = False
        self.map_mode_i = 0
        
        self.scale = 0.01
        self.ll = (55.753544, 37.621202)
        self.point = None  # type: str|None

        self.address = None  # type: str|None
        self.postcode = None  # type: str|None
        self.show_postcode = False

    def get_adderss(self):
        if self.address is None:
            return None
        
        return f"{self.address} ({self.postcode})" if self.show_postcode else self.address

    def get_ll_by_click(self, x: float, y: float) -> tuple[float, float]:
        center = (Map.STATIC_MAP_SIZE[0] / 2, Map.STATIC_MAP_SIZE[1] / 2)
        delta = (x - center[0], y - center[1])
        real_map_size = 2 * self.scale
        
        real_pixel_size_x = real_map_size / Map.STATIC_MAP_SIZE[0]
        real_pixel_size_y = real_map_size / Map.STATIC_MAP_SIZE[1]
        
        return (delta[1] * real_pixel_size_y, delta[0] * real_pixel_size_x)
        

    def change_ll(self, delta_lon: float, delta_lat: float):
        self.ll = (self.ll[0] + delta_lon, self.ll[1] + delta_lat)

    def change_scale(self, scale_up: bool):
        if scale_up:
            self.scale *= 10
        else:
            self.scale *= 0.1

    def toggle_postcode(self):
        self.show_postcode = not self.show_postcode

    def toggle_dark(self):
        self.is_dark = not self.is_dark

    def cycle_map_mode(self):
        self.map_mode_i = (self.map_mode_i + 1) % 3

    def find(self, geocode: str):
        geocoder_params = {
            "apikey": Map.GEOCODER_KEY,

            "geocode": geocode,
            "lang": "ru_RU",

            "format": "json"
        }
        
        response = must_respond(requests.get(Map.GEOCODER_API_SERVER, params=geocoder_params))
        body = response.json()
        toponym = body["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

        ll = toponym["Point"]["pos"]
        self.ll = tuple(map(float, ll.split(" ")))
        self.point = ",".join(ll.split(" ")) + ",pm2gnl"
       
        address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]
        self.address = address["formatted"]
        self.postcode = address["postal_code"]
    
    def find_by_ll(self, lon: float, lat: float):
        self.find(f"{lat}, {lon}")
    
    def find_organisation(self, lon: float, lat: float):
        distance = 50 * Map.DEGREES_IN_METER
        search_maps_params = {
            "apikey": Map.SEARCH_MAPS_KEY,
            "type": "biz",

            "text": f"{lat}, {lon}",
            "lang": "ru_RU",

            "ll": f"{lon},{lat}",
            "spn": f"{distance},{distance}",
            "rspn": 1,

            "format": "json"
        }
        
        response = must_respond(requests.get(Map.SEARCH_MAPS_API_SERVER, params=search_maps_params))
        body = response.json()
        
        features = body["features"]
        if len(features) == 0:
            return
        
        organisation = features[0]
        
        addr = organisation["properties"]["CompanyMetaData"]["Address"]
        self.address = addr["formatted"]
        self.postcode = addr["postal_code"]

        ll = organisation["geometry"]["coordinates"]
        self.point = ",".join(ll) + ",pm2gnl"

    def save_static_map(self):
        static_maps_params = {
            "apikey": Map.STATIC_MAPS_KEY,

            "ll": ",".join(map(str, self.ll)),
            "spn": f"{self.scale},{self.scale}",
            "size": ",".join(map(str, Map.STATIC_MAP_SIZE)),

            "lang": "ru_RU",
            "style": Map.MODES[self.map_mode_i],
            "theme": "dark" if self.is_dark else "light",
            "pt": self.point,
        }


        response = must_respond(requests.get(Map.STATIC_MAPS_API_SERVER, params=static_maps_params))

        with open(Map.STATIC_MAP_FILE, "wb") as file:
            file.write(response.content)

    def reset_point(self):
        self.point = None
        self.address = None
        self.postcode = None
        


        
