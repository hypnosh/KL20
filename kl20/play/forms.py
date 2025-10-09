from django import forms

# Form for a single answer and submit button
class AnswerForm(forms.Form):
	answer = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'placeholder': 'Your answer here'}))

# Login form with username and password
class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'placeholder': ''}))
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={ 'class': 'form-control' }))