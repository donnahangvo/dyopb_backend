# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# from .models import UserProfile

# class UserProfileForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)

#         self.fields['address'].widget.attrs['class'] = 'input'
#         self.fields['apartment'].widget.attrs['class'] = 'input'
#         self.fields['city'].widget.attrs['class'] = 'input'
#         self.fields['state'].widget.attrs['class'] = 'input'
#         self.fields['zipcode'].widget.attrs['class'] = 'input'
#         self.fields['country'].widget.attrs['class'] = 'input'
#         self.fields['phone'].widget.attrs['class'] = 'input'

#     class Meta:
#         model = UserProfile
#         fields = '__all__'
#         exclude = ('user',)

# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=50, required=True)
#     last_name = forms.CharField(max_length=50, required=True)
#     email = forms.EmailField(max_length=255, required=True)

#     def __init__(self, *args, **kwargs):
#         super(SignUpForm, self).__init__(*args, **kwargs)

#         self.fields['username'].widget.attrs['class'] = 'input'
#         self.fields['email'].widget.attrs['class'] = 'input'
#         self.fields['password1'].widget.attrs['class'] = 'input'
#         self.fields['password2'].widget.attrs['class'] = 'input'
#         self.fields['first_name'].widget.attrs['class'] = 'input'
#         self.fields['last_name'].widget.attrs['class'] = 'input'

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']