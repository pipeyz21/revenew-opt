import pandas as pd
from typing import Union, IO
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """
    DataLoader lee un CSV desde ruta o stream y lo convierte en DataFrame, 
    validando esquema mínimo y tipos.

    Args:
        csv_source: ruta (str) o input de Django (IO) con un csv.
    """
    def __init__(self, csv_source: Union[str, IO]):
        self.csv_source = csv_source

    def load(self) -> pd.DataFrame:
        """
        Retorna:
            pd.DataFrame con las columnas requeridas

        Raises:
            ValuerError: si el archivo no es CSV o faltan columnas
            pd.errors.ParseError: si pandas no puede parsear el csv
        """
        logger.info(f"Cargando CSV desde {self.csv_source}")

        # Si es ruta, validamos extensión
        if isinstance(self.csv_source, str) and not self.csv_source.endswith(".csv"):
            raise ValueError(f"El archivo debe tener extensión .csv")
        
        # Leemos el archivo CSV
        df = pd.read_csv(self.csv_source)
        logger.info("CSV cargado")

        # Validar columnas
        required = {
            "Product_A_Production_Time_Machine_1", 
            "Product_A_Production_Time_Machine_2", 
            "Product_B_Production_Time_Machine_1", 
            "Product_B_Production_Time_Machine_2",
            "Machine_1_Available_Hours", 
            "Machine_2_Available_Hours",
            "Price_Product_A",
            "Price_Product_B"
        }
        
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Columnas faltantes: {missing}")
        
        logger.info("Validación de columnas completada")
        
        # Validar tipos númericos
        for col in required:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(f"Columna {col} debe ser numérica")

        logger.info("Validación de tipos numéricos completada")

        return df