from django import forms


class share_form(forms.Form):
    title = forms.CharField(max_length=20)
    send = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(max_length=50, required=False, widget=forms.Textarea)
