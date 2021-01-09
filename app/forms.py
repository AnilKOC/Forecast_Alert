from django import forms

class Contact_form(forms.Form):
    name = forms.CharField(label='Your name ', max_length=200)
    mail = forms.EmailField(label='Mail ', max_length=200)
    message = forms.CharField(label='Message ', max_length=5000)

