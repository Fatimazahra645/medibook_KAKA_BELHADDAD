from django import forms
class PatientProfileForm(forms.Form):
    first_name=forms.CharField(max_length=150,required=False,label="Prenom",widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(max_length=150,required=False,label="Nom",widget=forms.TextInput(attrs={"class":"form-control"}))
    email=forms.EmailField(required=False,label="Email",widget=forms.EmailInput(attrs={"class":"form-control"}))
    phone=forms.CharField(max_length=20,required=False,label="Telephone",widget=forms.TextInput(attrs={"class":"form-control"}))
    birth_date=forms.DateField(required=False,label="Date de naissance",widget=forms.DateInput(attrs={"class":"form-control","type":"date"}))
