import io
import base64
import numpy as np
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
            - capacity (Tuple[float, float]): capacidades de las máquinas
            - used (Tuple[float, float]): horas usadas de las máquinas

    Raises:
        KeyError: Si falta alguna de las claves mínimas en el resultado.

    Attributes:
        raw (Dict[str, Any]): Almacena el resultado bruto del modelo.

    Methods:
        get_context() -> Dict[str, Any]: Devuelve un contexto listo para pasar a Django
        get_chart_base64() -> str: Genera y devuelve el gráfico de cantidades como base 64
    """

    def __init__(self, raw: Dict[str, Any]):
        # Validar que vengan las claves mínimas
        for key in ("status", "solution", "objective", "capacity", "used"):
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
            "capacity": self.raw["capacity"],
            "used": self.raw["used"],
        }
    
    def get_chart_base64(self) -> str:
        """
        Genera un gráfico con dos subplots:
        - Izquierda: cantidades óptimas por producto (gráfico de barras horizontal).
        - Derecha: comparación de horas usadas vs. capacidad para cada máquina (gráfico de barras agrupadas).

        Returns:
            str: Imagen codificada en base64 lista para ser embebida en HTML.
        """
        solution = self.raw["solution"]
        usage = self.raw["used"]
        capacity = self.raw["capacity"]

        products = list(solution.keys())
        quantities = list(solution.values())

        # Extraer uso y capacidad de cada máquina
        use1, use2 = usage if isinstance(usage, tuple) else (None, None)
        cap1, cap2 = capacity if isinstance(capacity, tuple) else (None, None)

        # Crear figura con dos subplots horizontales
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 4))

        # --- Subplot 1: Cantidades por producto ---
        y_pos = np.arange(len(products))
        ax1.barh(y_pos, quantities, edgecolor='black', alpha=0.7)
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(products)
        ax1.set_xlabel("Cantidad")
        ax1.set_title("Producción Óptima")

        # Añadir etiquetas numéricas al final de cada barra
        for i, v in enumerate(quantities):
            ax1.text(v + max(quantities)*0.01, i, str(v), va='center')

        # --- Subplot 2: Uso vs Capacidad de máquinas ---
        labels = ["M1", "M2"]
        usage_vals    = [use1, use2]
        capacity_vals = [cap1, cap2]

        x = np.arange(len(labels))
        width = 0.35

        # Barras agrupadas: uso y capacidad para cada máquina
        ax2.bar(x - width/2, usage_vals,    width, label="Uso")
        ax2.bar(x + width/2, capacity_vals, width, label="Capacidad")
        ax2.set_xticks(x)
        ax2.set_xticklabels(labels)
        ax2.set_ylabel("Horas")
        ax2.set_title("Uso vs Capacidad")
        ax2.legend()

        plt.tight_layout()

        # Guardar la figura en un buffer y codificarla en base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("ascii")