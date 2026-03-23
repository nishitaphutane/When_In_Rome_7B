from django import forms
from django.contrib.auth.models import User
from WhenInRome.models import UserProfile
from WhenInRome.models import Recommendation, City

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'picture',)   

class RecommendationForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the recommendation.")
    url = forms.URLField(max_length=200,
                         help_text="Please enter the URL of the recommendation.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Recommendation
        exclude = ('city',)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data
    
class CityForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the city name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = City
        fields = ('name',)