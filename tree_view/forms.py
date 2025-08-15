from django import forms
from .models import HsCode

class NoArrowInp(forms.ModelForm):
    class Meta:
        model = HsCode
        fields = "__all__"
        widgets = {
            "import_fee": forms.TextInput(attrs={"type": "text"})  # ✅ Forces text input (removes arrows)
        }
    # def clean_exp_ser_Fe(self):
    #     value = self.cleaned_data.get('export_fee')
    #     return value if value is not None else 0  # Convert NULL to 0
