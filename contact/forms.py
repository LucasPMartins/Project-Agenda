from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from contact.models import Contact

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Escreva seu primeiro nome',
            }
        ),
        help_text='Required. 50 characters or fewer.',
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Escreva seu telefone',
            }
        ),
        help_text='Required. 20 characters or fewer.',
    )

    class Meta:
        model = Contact
        fields = ('first_name',
                  'last_name',
                  'email',
                  'phone',
                  'description',
                  'category',
                  'picture',)
 

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError(
                'Primeiro nome não pode ser igual ao segundo',
                code='invalid'
            )
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)

        return super().clean()
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name == 'admin':
            raise ValidationError('Invalid first name')
        return first_name

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=50,
        error_messages={
            'required': 'This field is required',
            'min_length': 'This field must contain at least 2 characters',
            'max_length': 'This field must contain at most 50 characters',
        }
    )
    last_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=50,
        error_messages={
            'required': 'This field is required',
            'min_length': 'This field must contain at least 2 characters',
            'max_length': 'This field must contain at most 50 characters',
        }
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'This field is required',
            'invalid': 'This field must contain a valid email address',
        }
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email',
                'username', 'password1', 'password2'
                )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Email already exists in the database, please choose another one',code='invalid')
                )
        return email