from django import forms


class NameForm(forms.Form):

    textInput = forms.CharField(widget=forms.Textarea)
