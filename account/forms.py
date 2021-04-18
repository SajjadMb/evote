from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import ElectionUser
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django import forms


class CustomUserCreationForm(UserCreationForm):

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password1']
        # authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(CustomUserCreationForm, self).form_valid(form)

    class Meta:
        model = ElectionUser
        fields = ('email','full_name','profile_photo','password1','password2')



class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = ElectionUser
        fields = UserChangeForm.Meta.fields