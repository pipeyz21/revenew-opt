from django.shortcuts import render
from .forms import UploadForm, ManualParamsForm
from .core.data_loader import DataLoader
from .core.optimization_model import OptimizationModel
from .core.results_handler import ResultsHandler
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    """
    Esta vista renderiza la página de inicio del optimizador.
    Permite elegir subir CSV, formulario manual o datos de ejemplo.
    """
    logger.info("Renderizando la página de inicio del optimizador")
    return render(request, "optimizador/index.html")

def upload_view(request):
    """
    Vista para subir CSV
    """
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data["csv_file"]
            logger.info(f"Formulario de carga CSV válido: {form.cleaned_data['csv_file'].name}")

            # Cargamos el DataFrame
            try:
                df = DataLoader(csv_file).load()
                logger.info(f"Dataframe cargado correctamente con {len(df)} filas y {len(df.columns)} columnas")
            except Exception as e:
                logger.error(f"Error al cargar el DataFrame: {e}")
                # Si hay un error, lo agregamos al formulario para mostrarlo
                form.add_error("csv_file", str(e))
                return render(request, "optimizador/upload.html", {'form': form})
            
            # Ejecutar la optimización
            try:
                result = OptimizationModel(df).solve()
                logger.info(f"Optimización ejecutada con estado {result['status']}")
            except Exception as e:
                logger.error(f"Error al ejecutar la optimización: {e}")
                form.add_error(None, "Error al ejecutar la optimización. Verifique los datos del CSV.")
                return render(request, "optimizador/upload.html", {'form': form})

            # Preparamos el contexto para la plantilla
            rh = ResultsHandler(result)
            context = rh.get_context()

            # Agregar gráfico
            context["chart"] = rh.get_chart_base64()
            # mostrar capacidades en la plantilla
            context["capacity1"] = df.iloc[0]["Machine_1_Available_Hours"]
            context["capacity2"] = df.iloc[0]["Machine_2_Available_Hours"]
            logger.info("Contexto preparado para la plantilla de resultados")

            # Renderizamos la plantilla de resultados
            return render(request, "optimizador/results.html", context)
    
    else:
        logger.warning("Formulario de carga de CSV no válido")
        form = UploadForm()

    return render(request, 'optimizador/upload.html', {'form': form})

def manual_view(request):
    """
    Vista para ingresar manualmente los parámetros parámetros de optimización.
    """
    if request.method == 'POST':
        form = ManualParamsForm(request.POST)
        if form.is_valid():
            logger.info("Formulario manual válido, procesando datos")

            # Construimos la fila única del CSV a partir del form
            data = {
                'Product_A_Production_Time_Machine_1': form.cleaned_data['time_a_m1'],
                'Product_A_Production_Time_Machine_2': form.cleaned_data['time_a_m2'],
                'Product_B_Production_Time_Machine_1': form.cleaned_data['time_b_m1'],
                'Product_B_Production_Time_Machine_2': form.cleaned_data['time_b_m2'],
                'Machine_1_Available_Hours': form.cleaned_data['machine_1'],
                'Machine_2_Available_Hours': form.cleaned_data['machine_2'],
                'Price_Product_A': form.cleaned_data['price_a'],
                'Price_Product_B': form.cleaned_data['price_b'],
            }
            
            df = pd.DataFrame([data])

            # Ejecutar la optimización
            try:
                result = OptimizationModel(df).solve()
                logger.info(f"Optimización ejecutada con estado {result['status']}")
            except Exception as e:
                logger.error(f"Error al ejecutar la optimización: {e}")
                form.add_error(None, "Error al ejecutar la optimización. Verifique los datos del CSV.")
                return render(request, "optimizador/manual.html", {'form': form})
            
            # Preparamos el contexto para la plantilla
            rh = ResultsHandler(result)
            context = rh.get_context()

            # Agregar gráfico
            context["chart"] = rh.get_chart_base64()
            # mostrar capacidades en la plantilla
            context["capacity1"] = df.iloc[0]["Machine_1_Available_Hours"]
            context["capacity2"] = df.iloc[0]["Machine_2_Available_Hours"]
            logger.info("Contexto preparado para la plantilla de resultados")

            # Renderizamos la plantilla de resultados
            return render(request, 'optimizador/results.html', context)
    else:
        form = ManualParamsForm()

    return render(request, 'optimizador/manual.html', {'form': form})

def test_view(request):
    """
    Vista para cargar datos de prueba.
    Carga un DataFrame predefinido y ejecuta la optimización.
    """
    logger.info("Cargando datos de prueba")
    
    # Cargamos el DataFrame con datos de prueba -> Se asume que estan en carpeta data
    try:
        df = DataLoader("data/optimization_problem_data.csv").load()
        logger.info(f"Dataframe cargado correctamente con {len(df)} filas y {len(df.columns)} columnas")
    except Exception as e:
        logger.error(f"Error al cargar el DataFrame: {e}")
        return render(request, "optimizador/index.html", {'error': "Error al cargar los datos de prueba. Verifique el archivo CSV."})
    
    # Ejecutar la optimización
    try:
        result = OptimizationModel(df).solve()
        logger.info(f"Optimización ejecutada con estado {result['status']}")
    except Exception as e:
        logger.error(f"Error al ejecutar la optimización: {e}")
        return render(request, "optimizador/index.html", {'error': "Error al ejecutar la optimización. Verifique los datos del CSV."})
    
    # Preparamos el contexto para la plantilla
    rh = ResultsHandler(result)
    context = rh.get_context()

    # Agregar gráfico
    context["chart"] = rh.get_chart_base64()
    # mostrar capacidades en la plantilla
    context["capacity1"] = df.iloc[0]["Machine_1_Available_Hours"]
    context["capacity2"] = df.iloc[0]["Machine_2_Available_Hours"]
    
    logger.info("Contexto preparado para la plantilla de resultados de prueba")

    # Renderizamos la plantilla de resultados
    return render(request, "optimizador/results.html", context)