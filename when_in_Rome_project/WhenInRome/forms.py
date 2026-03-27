from django import forms
from django.contrib.auth.models import User
from WhenInRome.models import UserProfile
from WhenInRome.models import Recommendation, City, Review, City

class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Choose a username'
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email (optional)'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Choose a password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('bio', 'picture')

class RecommendationForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    location = forms.CharField(max_length=256, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Recommendation
        fields = ('title', 'location', 'description', 'image')
    
class CityForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the city name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = City
        fields = ('name',)

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        help_text="Rating must be between 1 and 5."
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Leave an optional comment."
    )

    class Meta:
        model = Review
        fields = ('rating', 'comment')


