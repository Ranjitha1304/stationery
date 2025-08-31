# mainapp/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=20,
        min_length=3,
        widget=forms.TextInput(attrs={"placeholder": "Enter your Name"}),
        error_messages={"required": "Name is required"}
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Enter Email ID"}),
        error_messages={"required": "Valid email is required"}
    )
    phone = forms.RegexField(
        regex=r'^\d{10}$',
        widget=forms.TextInput(attrs={"placeholder": "Enter your number"}),
        error_messages={"invalid": "Enter a valid 10 digit phone number"}
    )
    message = forms.CharField(
        min_length=5,
        max_length=30,
        widget=forms.Textarea(attrs={"placeholder": "Enter Message", "rows": 3}),
        error_messages={"required": "Message is required"}
    )
