from django import forms

from tambolaapp.models import *

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title','content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title' : 'Enter title:',
            'content': 'Enter a Content: ',
        }