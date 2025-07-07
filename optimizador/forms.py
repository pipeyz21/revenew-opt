from django import forms
from django.core.validators import FileExtensionValidator

class UploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Archivo CSV",
        validators=[FileExtensionValidator(["csv"])],
        help_text="Solo archivos .csv"
    )

class ManualParamsForm(forms.Form):
    price_a = forms.FloatField(label="Precio Producto A", min_value=0)
    price_b = forms.FloatField(label="Precio Producto B", min_value=0)
    time_a_m1 = forms.FloatField(label="Tiempo A en Máquina 1", min_value=0)
    time_b_m1 = forms.FloatField(label="Tiempo B en Máquina 1", min_value=0)
    time_a_m2 = forms.FloatField(label="Tiempo A en Máquina 2", min_value=0)
    time_b_m2 = forms.FloatField(label="Tiempo B en Máquina 2", min_value=0)
    machine_1 = forms.FloatField(label="Horas Máquina 1", min_value=0)
    machine_2 = forms.FloatField(label="Horas Máquina 2", min_value=0)
