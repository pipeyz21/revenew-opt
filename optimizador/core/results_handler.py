import io
import base64
from typing import Dict, Any
import matplotlib.pyplot as plt

class ResultsHandler:
    """
    Procesa los resultados del OptimizationModel para la capa visual.

    Args:
        result: dict con claves
            - status (str): estado del solver.
            - solution (Dict[str, int]): cantidades óptimas por producto
            - objective (float): ingreso total óptimo
    """

    def __init__(self, raw: Dict[str, Any]):
        # Validar que vengan las claves mínimas
        for key in ("status", "solution", "objective"):
            if key not in raw:
                raise KeyError(f"Falta clave '{key}' en el resultado de optimización")
        
        self.raw = raw

    def get_context(self) -> Dict[str, Any]:
        """
        Devuelve un contexto listo para pasar a Django
        """
        return {
            "status": self.raw["status"],
            "solution": self.raw["solution"],
            "objective": self.raw["objective"],
        }
    
    def get_chart_base64(self) -> str:
        """
        Genera y devuelve el gráfico de cantidades como base64
        """
        solution = self.raw["solution"]
        products = list(solution.keys())
        quantities = list(solution.values())

        plt.figure(figsize=(6, 4))
        plt.bar(products, quantities)
        plt.title("Producción Óptima")
        plt.xlabel("Producto")
        plt.ylabel("Cantidad")
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)

        return base64.b64encode(buffer.read()).decode("ascii")