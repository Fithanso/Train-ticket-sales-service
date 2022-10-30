class VoyageDisplayObject:

    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __str__(self):
        if hasattr(self, 'departure_station') and hasattr(self, 'arrival_station'):
            return self.departure_station.name + ' - ' + self.arrival_station.name
        return ''
