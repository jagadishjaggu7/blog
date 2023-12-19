from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from blog.models import Post

from blog.views import PostCreateView
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']     

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                'this account is not registered please register',
                code='inactive',
            )
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']        
        
class PasswordResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)



