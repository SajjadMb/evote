from django import forms


class profileForm(forms.Form):
    user_fullname = forms.CharField(required=False)
    user_job = forms.CharField(required=False)
    user_photo = forms.ImageField(required=False)