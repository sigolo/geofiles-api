from .db_models import CustomLayers as CustomLayersTable
from .db_engine import database
from ..api.schemas import TokenData

SUPPORTED_FORMAT = [".shp", ".dwg", ".json", ".csv"]