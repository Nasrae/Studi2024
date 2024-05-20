import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Important pour la connexion."}),
        required=True
    )
    first_name = forms.CharField(
        label='Nom',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom'})
    )
    last_name = forms.CharField(
        label='Prénom',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre prénom'})
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Entrez votre mot de passe'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmation du mot de passe'}),
        strip=False,
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Entrez votre adresse email'})
    )


    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name", "password1", "password2")
