import io
import base64
from typing import Dict, Any
# import matplotlib.pyplot as plt

class ResultsHandler:
    """
    Procesa los resultados del OptimizationModel para la capa visual.

    Args:
        result: dict con claves
            - status (str): estado del solver.
            - solution (Dict[str, int]): cantidades óptimas por producto
            - objective (float): ingreso total óptimo
    """

    def __init__(self, result: Dict[str, Any]):
        self.status: str = result["stats"]
        self.solution: Dict[str, int] = result["solution"]
        self.objective: float = result["objective"]

    def to_dict(self) -> Dict[str, Any]:
        """
        Devuelve un contexto listo para pasar a Django
        """
        return {
            "status": self.status,
            "solution": self.solution,
            "objective": self.objective,
        }
    
    # def plot_solution(self) -> str: