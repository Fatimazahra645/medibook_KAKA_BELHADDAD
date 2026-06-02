from django import forms
from .models import Review, Availability




class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review; fields=["rating","comment"]
        widgets={"rating":forms.Select(attrs={"class":"form-select"}),
                 "comment":forms.Textarea(attrs={"rows":4,"class":"form-control"})}


class DoctorProfileForm(forms.Form):
    first_name=forms.CharField(max_length=150,required=False,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(max_length=150,required=False,widget=forms.TextInput(attrs={"class":"form-control"}))
    email=forms.EmailField(required=False,widget=forms.EmailInput(attrs={"class":"form-control"}))
    phone=forms.CharField(max_length=20,required=False,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(max_length=255,required=False,widget=forms.TextInput(attrs={"class":"form-control"}))
    bio=forms.CharField(required=False,widget=forms.Textarea(attrs={"rows":3,"class":"form-control"}))
    experience_years=forms.IntegerField(required=False,min_value=0,widget=forms.NumberInput(attrs={"class":"form-control"}))
    image=forms.ImageField(required=False)

    
class AvailabilityForm(forms.ModelForm):
    class Meta:
        model=Availability; fields=["day_of_week","start_time","end_time"]
        widgets={"day_of_week":forms.Select(attrs={"class":"form-select"}),
                 "start_time":forms.TimeInput(attrs={"class":"form-control","type":"time"}),
                 "end_time":forms.TimeInput(attrs={"class":"form-control","type":"time"})}
