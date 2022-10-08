
from .models import Profile, Bookings
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
import datetime

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'age', 'status']

class BookingsForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['date_time','name', 'stats']
        widgets = {
            'date_time': DateTimePickerInput(
                options = {
                    'minDate': (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00'),
                    'maxDate': (datetime.datetime.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d 23:59:59'),
                    'enabledHours': [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                    'showTodayButton' : False,
                }
            )
        }    

    def __init__(self, *args, **kwargs):
        super(BookingsForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs['readonly'] = True
        self.fields["stats"].widget.attrs['readonly'] = True
    
    def clean(self):
        name = self.cleaned_data['name']
        date_time = self.cleaned_data['date_time']
        if Bookings.objects.filter(name=name).filter(date_time=date_time):
            raise forms.ValidationError("Booked Already")
        
            

