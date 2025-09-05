from django import forms
from .models import  CustomUser, SeekerProfile, RecruiterProfile, Job



class customeUserUpateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['display_name','email']
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your display name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }
class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = SeekerProfile
        fields = ['full_name', 'phone', 'resume', 'skills', 'experience', 'location', 'profile_picture']
        widgets = {
            
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List your skills separated by commas'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your years of experience'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your location'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        
class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = [
            
            'company_name',
            'contact_person',
            'phone',
            'company_website',
            'location',
            'profile_picture',
            'company_description'
        ]
        widgets = {
           
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your company name'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'company_website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.yourcompany.com'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company location'
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'company_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your company, its mission, and culture...'
            }),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
    'title','category','job_type','location',
    'experience_required','skills','salary_min',
    'salary_max','description','application_deadline',
]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'experience_required': forms.Select(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
