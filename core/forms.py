# forms.py
from django import forms
from .models import Reservation  # Assuming your model is named 'Reservation'

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['user', 'date', 'time', 'guests', 'status']
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Adjust formats as needed
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        input_formats=['%H:%M'],  # Adjust formats as needed
    )



from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User  # Import your custom user model

# Custom user creation form for signup
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'email', 'phone_number', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'role', 'phone_number')

# Custom authentication form for login
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')




# forms.py
from django import forms
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['menugroup', 'name', 'price', 'description', 'image', 'available']


from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']


from .models import Menu, MenuGroup

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description', 'is_active', 'image']

class MenuGroupForm(forms.ModelForm):
    class Meta:
        model = MenuGroup
        fields = ['menu', 'name', 'description', 'parent_group', 'is_active', 'image']