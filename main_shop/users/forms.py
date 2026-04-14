from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.html import strip_tags
from django.core.validators import RegexValidator

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=254, widget=forms.EmailInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Last Name'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = None   # у нас нет поля username
        if commit:
            user.save()
        return user

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Password'}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data

class CustomUserChangeForm(forms.ModelForm):
    phone_number = forms.CharField(required=False, max_length=20,
                            widget=forms.TextInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Phone'}),
                            validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Enter a valid phone number")])
    first_name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, max_length=254, widget=forms.EmailInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'company', 'address1', 'address2', 'city', 'country', 'province', 'postal_code', 'phone_number']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Company'}),
            'address1': forms.TextInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Address line 1'}),
            'address2': forms.TextInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Address line 2'}),
            'city': forms.TextInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'City'}),
            'country': forms.Select(attrs={'class': 'border border-gray-200 w-full py-2 px-3 text-sm focus:outline-none focus:border-black'}),
            'province': forms.Select(attrs={'class': 'border border-gray-200 w-full py-2 px-3 text-sm focus:outline-none focus:border-black'}),
            'postal_code': forms.TextInput(attrs={'class': 'dotted-input w-full', 'placeholder': 'Postal code'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('email'):
            cleaned_data['email'] = self.instance.email
        for field in ['company', 'address1', 'address2', 'city', 'country', 'province', 'postal_code', 'phone_number']:
            print(field, cleaned_data.get(field))
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])
        return cleaned_data