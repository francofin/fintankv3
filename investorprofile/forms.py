from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Portfolio_2
from django import forms


class PortfolioForm(forms.ModelForm):
    class Meta():
        model = Portfolio_2
        fields = ['ticker']
        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user','')
            super(PortfolioForm, self).__init__(*args, **kwargs)
            self.fields['ticker']=forms.ModelChoiceField(queryset=Portfolio_2.objects.filter(user=user))
