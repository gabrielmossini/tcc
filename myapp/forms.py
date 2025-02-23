from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        else:  
            user.password = User.objects.get(pk=self.instance.pk).password
        
        if commit:
            user.save()
        return user
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'cpf', 'birthday']