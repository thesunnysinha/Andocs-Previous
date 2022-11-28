from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm,UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer,Profile,Comment

GENDER_CHOICES = (
    ('Male','Male'),
    ('Female','Female'),
    ('Prefer Not to Say','Prefer Not to Say'),
)
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='First Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Last Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    phone_num = forms.IntegerField(max_value=9999999999,min_value=1000000000)
    gender = forms.ChoiceField(choices = GENDER_CHOICES)
    profile_pic = forms.ImageField()
    class Meta:
        model = User
        fields = [
            'first_name','last_name','username', 'email', 'password1', 'password2',
            'phone_num','gender','birth_date','profile_pic'
        ]
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label=_('New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField( label=_("Email"), max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))
    

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer 
        fields = ['name','locality','city','state','zipcode','mobile_number']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
                  'locality':forms.TextInput(attrs={'class':'form-control'}),
                  'city':forms.TextInput(attrs={'class':'form-control'}),
                  'state':forms.Select(attrs={'class':'form-control'}),
                  'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
                  'mobile_number': forms.NumberInput(attrs={'class':'form-control'}),
                }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_num','gender','birth_date','profile_pic']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject','comment','rating']