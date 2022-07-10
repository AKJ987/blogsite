from django import forms
from django.forms import ModelForm
from blogapp.models import UserProfile, Blogs, Comments
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']

    

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=('user',)

        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control','placeholder':'Bio'}),
            'phone': forms.TextInput(attrs={'class': 'form-control','placeholder':'Phone Number'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control','type':'date'})
        }

class PasswordResetForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput())
    new_password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField()

class BlogForm(forms.ModelForm):
    class Meta:
        model=Blogs
        fields=['title','description','image']

        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

        widgets = {
            'comment': forms.TextInput(attrs={'class': 'form-control'})
        }



