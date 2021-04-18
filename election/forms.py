from django import forms
from django.forms import formset_factory


from django import forms
from django.forms import formset_factory


class CandidateForm(forms.Form):
    candidate_firstName = forms.CharField(required=True,label='نام',widget=forms.TextInput(attrs={'class' : 'form-field1'}))
    candidate_lastName = forms.CharField(required=True,label='نام خانوادگی',widget=forms.TextInput(attrs={'class' : 'form-field1'}))
    candidate_email =forms.EmailField(required=True,label='ایمیل',widget=forms.TextInput(attrs={'class' : 'form-field1'}))
    candidate_description=forms.CharField(required=True,label='توضیحات',widget=forms.TextInput(attrs={'class' : 'form-field1'}))
    candidate_photo=forms.ImageField(required=False,label='آپلود تصویر',widget=forms.FileInput(attrs={'accept':'.jpg,.png','type' : 'file','id':'candidate-photo'}))


class ElectionForm(forms.Form):
    election_name = forms.CharField(required=True,label='عنوان انتخابات',widget=forms.TextInput(attrs={'type' : 'text','id' :'title' ,'class' : 'form-field','name':'title'}))
    election_des = forms.CharField(required=True,label='توضیحات انتخابات',widget=forms.TextInput(attrs={'type' : 'text','id' :'des' ,'class' : 'form-field','name':'des'}))
    start_date = forms.DateField(required=True,input_formats=['%d-%m-%Y','%Y-%m-%d'],label='زمان آغاز رای گیری',widget=forms.TextInput(attrs={'type' : 'text','data-field' :'date'}))
    end_date = forms.DateField(required=True,input_formats=['%d-%m-%Y','%Y-%m-%d'],label='زمان پایان رای گیری',widget=forms.TextInput(attrs={'type' : 'text','data-field' :'date'}))
    election_voter=forms.FileField(required=False,label='انتخاب رأی دهندگان',widget=forms.FileInput(attrs={'accept':'.csv','type' : 'file','name':'election_voter','id':'id_election_voter'}))


CandidateFormSet = formset_factory(CandidateForm,min_num=1)


class NationalCodeForm(forms.Form):
    national_code = forms.CharField(required=True)


