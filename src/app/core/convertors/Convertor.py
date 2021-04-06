from abc import ABC, abstractmethod



class Convertor(ABC):

    @abstractmethod
    def to_shp(self):
        pass

    @abstractmethod
    def to_dwg(self):
        pass

    @abstractmethod
    def to_geojson(self):
        pass

    @abstractmethod
    def to_csv(self):
        pass
