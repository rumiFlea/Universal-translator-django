from django import forms

class SpeechToTextForm(forms.Form):
    audio = forms.FileField()
