from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
     USER_CHOICES = (
        ('recruiter', 'Recruiter'),
        ('job_seeker', 'Job Seeker'),
      )
     user_type = models.CharField(max_length=20, choices=USER_CHOICES)
     display_name = models.CharField(max_length=100, null=True, blank=True)

class SeekerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='seeker_profile')
    full_name = models.CharField(max_length=100,null=True, blank=True)
    phone= models.CharField(max_length=15,null=True, blank=True)
    resume = models.FileField(upload_to='resumes/',null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=100,null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
class RecruiterProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='recruiter_profile')
    company_name = models.CharField(max_length=100,null=True, blank=True)
    contact_person = models.CharField(max_length=100,null=True, blank=True)
    phone= models.CharField(max_length=15,null=True, blank=True)
    company_website = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=100,null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',null=True, blank=True)
    company_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    

    
class Job(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('remote', 'Remote'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    category_choices = [
        ('IT', 'Information Technology'),
        ('HR', 'Human Resources'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Education', 'Education'),
        ('Healthcare', 'Healthcare'),
        ('Engineering', 'Engineering'),
        ('Hospitality', 'Hospitality'),
        ('Real Estate', 'Real Estate'),
        ('Other', 'Other'),
    ]

    recruiter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200,null=True, blank=True)
    category = models.CharField(max_length=100, choices=category_choices, null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100,null=True, blank=True)
    EXPERIENCE_CHOICES = [
        (1, '0-2 years'),
        (2, '3-5 years'),
        (3, '6-10 years'),
        (4, '10+ years'),
    ]
    experience_required = models.IntegerField(choices=EXPERIENCE_CHOICES, null=True, blank=True)
    skills = models.TextField(help_text="Comma-separated skills, e.g. React, JavaScript, CSS", null=True, blank=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time',null=True, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    seeker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('interviewed', 'Interviewed'),
        ('offered', 'Offered'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.seeker.username} - {self.job.title}"
