from django import forms

# Form for a single answer and submit button
class AnswerForm(forms.Form):
	answer = forms.CharField(label='Answer', max_length=50)

# Login form with username and password
class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=150)
	password = forms.CharField(label='Password', widget=forms.PasswordInput)