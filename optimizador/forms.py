from django import forms
from django.core.validators import FileExtensionValidator

class UploadForm(forms.Form):
    """
    Formulario para subir un archivo CSV con los datos de optimización.
    
    Campos:
        - csv_file: Campo para subir un archivo CSV. (Validado para aceptar solo archivos con extensión .csv)
    """
    csv_file = forms.FileField(
        label="Archivo CSV",
        validators=[FileExtensionValidator(["csv"])],
        help_text="Solo archivos .csv"
    )

class ManualParamsForm(forms.Form):
    """
    Formulario para ingresar parámetros manualmente para la optimización.
    Campos:
        - price_a: Precio del Producto A.
        - price_b: Precio del Producto B.
        - time_a_m1: Tiempo del Producto A en la Máquina 1.
        - time_b_m1: Tiempo del Producto B en la Máquina 1.
        - time_a_m2: Tiempo del Producto A en la Máquina 2.
        - time_b_m2: Tiempo del Producto B en la Máquina 2.
        - machine_1: Horas disponibles de la Máquina 1.
        - machine_2: Horas disponibles de la Máquina 2.
    Todos los campos son obligatorios y deben ser números positivos.
    """
    price_a = forms.FloatField(label="Precio Producto A", min_value=0)
    price_b = forms.FloatField(label="Precio Producto B", min_value=0)
    time_a_m1 = forms.FloatField(label="Tiempo A en Máquina 1", min_value=0)
    time_b_m1 = forms.FloatField(label="Tiempo B en Máquina 1", min_value=0)
    time_a_m2 = forms.FloatField(label="Tiempo A en Máquina 2", min_value=0)
    time_b_m2 = forms.FloatField(label="Tiempo B en Máquina 2", min_value=0)
    machine_1 = forms.FloatField(label="Horas Máquina 1", min_value=0)
    machine_2 = forms.FloatField(label="Horas Máquina 2", min_value=0)
