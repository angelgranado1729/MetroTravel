

class Data:
    def __init__(self):
        self.flights = [
            ('CCS', 'AUA', 40),
            ('CCS', 'CUR', 35),
            ('CCS', 'BON', 60),
            ('CCS', 'SXM', 300),
            ('AUA', 'CUR', 15),
            ('AUA', 'BON', 15),
            ('CUR', 'BON', 15),
            ('CCS', 'SDQ', 180),
            ('SDQ', 'SXM', 50),
            ('SXM', 'SBH', 45),
            ('CCS', 'POS', 150),
            ('POS', 'BGI', 35),
            ('POS', 'SXM', 90),
            ('BGI', 'SXM', 70),
            ('POS', 'PTP', 80),
            ('POS', 'FDF', 75),
            ('PTP', 'SXM', 100),
            ('PTP', 'SBH', 80),
            ('CUR', 'SXM', 70),
            ('AUA', 'SXM', 85)
        ]

        self.visas = {
            'CCS': False,
            'AUA': True,
            'BON': True,
            'CUR': True,
            'SXM': True,
            'SDQ': True,
            'SBH': False,
            'POS': False,
            'BGI': False,
            'PTP': False,
            'FDF': False
        }

        self.airports = {
            'CCS': 'Caracas',
            'AUA': 'Aruba',
            'BON': 'Bonaire',
            'CUR': 'Curazao',
            'SXM': 'Sint Maarten',
            'SDQ': 'Santo Domingo',
            'SBH': 'Saint Barth',
            'POS': 'Port of Spain (Trinidad)',
            'BGI': 'Bridgetown',
            'PTP': 'Pointe-a-Pitre (Guadalupe)',
            'FDF': 'Fort-de-France (Martinique)'
        }

        self.codes = [
            'CCS',
            'AUA',
            'BON',
            'CUR',
            'SXM',
            'SDQ',
            'SBH',
            'POS',
            'BGI',
            'PTP',
            'FDF'
        ]

        self.vertices = {
            'CCS': 0,
            'AUA': 1,
            'BON': 2,
            'CUR': 3,
            'SXM': 4,
            'SDQ': 5,
            'SBH': 6,
            'POS': 7,
            'BGI': 8,
            'PTP': 9,
            'FDF': 10
        }

    def get_flights(self):
        return self.flights

    def get_visas(self):
        return self.visas

    def get_airports(self):
        return self.airports

    def get_airport_name(self, airport):
        return self.airports[airport]

    def get_vertex(self, airport):
        return self.vertices[airport]

    def __str__(self):
        return f'Flights: {self.flights}\nVisas: {self.visas}\nAirports: {self.airports}\nVertices: {self.vertices}'
