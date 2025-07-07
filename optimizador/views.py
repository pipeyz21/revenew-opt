from django.shortcuts import render
from .forms import UploadForm, ManualParamsForm
from .core.data_loader import DataLoader
from .core.optimization_model import OptimizationModel
from .core.results_handler import ResultsHandler
import pandas as pd

# Create your views here.
def index(request):
    """
    Landing page: elige subir CSV o formulario manual
    """
    return render(request, "optimizador/index.html")

def upload_view(request):
    """
    Vista para subir CSV
    """
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data["csv_file"]

            # Cargamos el DataFrame
            try:
                df = DataLoader(csv_file).load()
            except Exception as e:
                form.add_error("csv_file", str(e))
            else:
                # Ejecutamos la optimización
                result = OptimizationModel(df).solve()
                rh = ResultsHandler(result)
                context = rh.get_context()

                # Agregar gráfico
                return render(request, "optimizador/results.html", context)
    
    else:
        form = UploadForm()

    return render(request, 'optimizador/upload.html', {'form': form})

def manual_view(request):
    """
    Vista para ingresar parámetros a mano.
    """
    if request.method == 'POST':
        form = ManualParamsForm(request.POST)
        if form.is_valid():
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
            
            # Ejecutamos optimización
            result = OptimizationModel(df).solve()
            rh = ResultsHandler(result)
            context = rh.get_context()
            context["chart"] = rh.get_chart_base64()

            return render(request, 'optimizador/results.html', context)
    else:
        form = ManualParamsForm()

    return render(request, 'optimizador/manual.html', {'form': form})