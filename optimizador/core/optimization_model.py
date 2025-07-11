from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value
import pandas as pd
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

class OptimizationModel:
    """
    OptimizationModel encapsula un problema de maximización de ingresos para 2 productos (A y B),
    usando los datos de una sola fila de un DataFrame con formato:
        Product_A_Production_Time_Machine_1,
        Product_A_Production_Time_Machine_2,
        Product_B_Production_Time_Machine_1,
        Product_B_Production_Time_Machine_2,
        Machine_1_Available_Hours,
        Machine_2_Available_Hours,
        Price_Product_A,
        Price_Product_B

    Args:
        df: DataFrame previamente validado.

    Attributes:
        cap1 (float): Capacidad de la máquina 1.
        cap2 (float): Capacidad de la máquina 2.
        products (List[str]): Lista de productos detectados.
        prices (Dict[str, float]): Mapa de precios por producto.  
        time1 (Dict[str, float]): Mapa de tiempos de producción en la máquina 1 por producto.
        time2 (Dict[str, float]): Mapa de tiempos de producción en la máquina
        model (LpProblem): Modelo de optimización de PuLP.
        vars (Dict[str, LpVariable]): Variables de decisión para cada producto.

    Methods:
        solve() -> Dict[str, Any]:
            Resuelve el modelo de optimización y devuelve un diccionario con:
                - status: estado del solver (str)
                - solution: dict {producto: cantidad_optima}
                - objective: ingreso total óptimo (float)
                - capacity: tuple con capacidades de las máquinas (float, float)
                - used: tuple con horas usadas de las máquinas (float, float)
    """
    def __init__(self, df: pd.DataFrame):

        # Asumimos que 'df' tiene exactamente 1 fila
        row = df.iloc[0]

        # Extraemos las capacidades de cada maquina
        self.cap1 = float(row["Machine_1_Available_Hours"])
        self.cap2 = float(row["Machine_2_Available_Hours"])
        logger.info("Extracción de capacidades completada")

        # Detectar productos
        price_cols = [p for p in row.index if p.startswith("Price_Product_")]
        self.products = [p.replace("Price_Product_", "") for p in price_cols]
        logger.info("Detección de productos completada")

        # Mapas de precios y tiempos
        self.prices = {p: float(row[f"Price_Product_{p}"]) for p in self.products}
        self.time1 = {p: float(row[f"Product_{p}_Production_Time_Machine_1"]) for p in self.products}
        self.time2 = {p: float(row[f"Product_{p}_Production_Time_Machine_2"]) for p in self.products}
        logger.info("Mapeo de precios y tiempos de producción completado")

        # Creamos el modelo de optimización
        self.model = LpProblem("Optimization_Model", LpMaximize)
        logger.info("Modelo creado")

        # Creamos variables de decisión, un entero >= 0 por producto
        self.vars = {p: LpVariable(f"x_{p}", lowBound=0, cat="Integer") for p in self.products}
        logger.info("Variables de decisión creadas")

    def _build_objective(self):
        """
        Función para maximizar ingresos diarios
           Max Z = Σ precio[p] * x_p
        """
        self.model += lpSum(self.prices[p] * self.vars[p] for p in self.products), "Objetivo"
        logger.info("Función objetivo añadida")

    def _add_constraints(self):
        # Restricción de Capacidad Máquina 1
        self.model += (lpSum(self.time1[p] * self.vars[p] for p in self.products) <= self.cap1, "Capacidad_M1")

        # Restricción de Capacidad Máquina 2
        self.model += (lpSum(self.time2[p] * self.vars[p] for p in self.products) <= self.cap2, "Capacidad_M2")

        logger.info("Restricciones añadidas")

    def solve(self) -> Dict[str, Any]:
        """
        Resuelve el modelo y devuelve:
            - status: estado del solve
            - solution: dict {producto: cantidad_optima}
            - objective: ingreso total
        Raises:
            RuntimeError si no encuentra solutión óptima o no se obtuvo el valor para una variable.
        """
        # Utilizamos las funciones privadas para construir el modelo
        logger.info("Construyendo el modelo de optimización...")
        self._build_objective()
        self._add_constraints()
        
        # Resolvemos el modelo
        logger.info("Resolviendo modelo...")
        status_code = self.model.solve()
        status = LpStatus[status_code]
        if status != "Optimal":
            raise RuntimeError(f"Solver no encontró solución óptima: {status}")
        
        # Extraer resultados
        logger.info("Extrayendo resultados...")
        solution = {}
        for p in self.products:
            val = self.vars[p].value()
            if val is None:
                raise RuntimeError(f"No se obtuvo valor para la variable de producto '{p}'")
            solution[p] = int(val)

        total = value(self.model.objective)

        if total is None:
            raise RuntimeError("No se pudo calcular el valor de la función objetivo")
        
        # Calcular uso de maquinas
        used1 = sum(self.time1[p] * solution[p] for p in self.products)
        used2 = sum(self.time2[p] * solution[p] for p in self.products)

        return {
            "status": status, 
            "solution": solution, 
            "objective": total,
            "capacity": (self.cap1, self.cap2),
            "used": (used1, used2)
        }