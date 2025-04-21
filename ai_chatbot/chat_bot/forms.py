from django import forms

class UserInput(forms.Form):
    user_input = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ask your question...'})
    )