from django.forms import ModelForm
from .models import Subsystem


class SubsystemForm(ModelForm):
    class Meta:
        model = Subsystem
        exclude = ['slug', 'owner']
