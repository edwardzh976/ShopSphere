from django import forms
from django.core.exceptions import ValidationError

class Form(forms.Form):
    title = forms.CharField(label='Title', max_length=30)
    desc = forms.CharField(label='Description', max_length=100)
    bid = forms.IntegerField(min_value=0, label='Starting Bid')
    pic = forms.ImageField()

#class CommentForm(forms.Form):
 #   comment = forms.CharField(label="Comment", max_length=100)