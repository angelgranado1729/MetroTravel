import csv

class Data:
    def __init__(self, flights_file, visas_file, airports_file):
        self.flights = self.load_flights(flights_file)
        self.visas = self.load_visas(visas_file)
        self.airports = self.load_airports(airports_file)
        self.codes = list(self.airports.keys())
        self.vertices = {code: index for index, code in enumerate(self.codes)}

    def load_flights(self, filename):
        flights = []
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                flights.append((row['origin'], row['destination'], int(row['cost'])))
        return flights

    def load_visas(self, filename):
        visas = {}
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                visas[row['airport']] = row['visa_required'].lower() == 'true'
        return visas

    def load_airports(self, filename):
        airports = {}
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                airports[row['code']] = row['name']
        return airports

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
