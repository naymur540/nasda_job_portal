from django.utils import timezone
from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout,update_session_auth_hash
from .models import *
from .froms import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q


def home(request):
    jobs= Job.objects.filter(application_deadline__gte=timezone.now()).order_by('-created_at')[:5]
    for job in jobs:
        job.skill_list = [s.strip() for s in (job.skills or '').split(',')]
    return render(request, 'home.html', {'jobs': jobs})
def register_page(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        display_name = request.POST['display_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_type = request.POST['user_type']
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        user = CustomUser.objects.create_user(username=username, password=password,email=email, user_type=user_type,display_name=display_name)
        user.save()
        if user_type == 'job_seeker':
            SeekerProfile.objects.create(user=user)
        else:
            RecruiterProfile.objects.create(user=user)
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')
    return render(request, 'signup.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if user.user_type == 'job_seeker':
                profile = getattr(user, 'seeker_profile', None)
                if not profile or not profile.full_name or not profile.skills:
                    return redirect('update_profile')

            elif user.user_type == 'recruiter':
                profile = getattr(user, 'recruiter_profile', None)
                if not profile or not profile.company_name or not profile.contact_person:
                    return redirect('update_profile')

            return redirect('home')

        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')
def logout_user(request):
    logout(request)
    return redirect('home')
def password_change(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = authenticate(request, username=request.user.username, password=current_password)
        if user is not None:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('dashboard')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(request, 'Current password is incorrect.')

    return render(request, 'password_change.html')



def profile_view(request):
    user = request.user
    if user.user_type == 'job_seeker':
        profile = user.seeker_profile
    else:
        profile = user.recruiter_profile

    skills_list = []
    if profile and getattr(profile, "skills", None):
        skills_list = [s.strip() for s in profile.skills.split(",") if s.strip()]

    return render(request, "profile.html", {
        "user": user,
        "profile": profile,
        "skills": skills_list,
    })


def update_profile(request):
    user = request.user
    user_form = customeUserUpateForm(request.POST or None, instance=user)

    if user.user_type == 'job_seeker':
        profile = getattr(user, 'seeker_profile', None)
        profile_form = SeekerProfileForm(request.POST or None, request.FILES or None, instance=profile)
    else:
        profile = getattr(user, 'recruiter_profile', None)
        profile_form = RecruiterProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')

    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'form': profile_form
    })


def dashboard(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'job_seeker':
            applied_jobs = Application.objects.filter(seeker=request.user).select_related('job', 'job__recruiter')
            for app in applied_jobs:
                app.job.skill_list = [s.strip() for s in (app.job.skills or '').split(',')]
            application_count = applied_jobs.count()
            interviews_count = applied_jobs.filter(status='interviewed').count()
            offers_count = applied_jobs.filter(status='offered').count()
            pending_count = applied_jobs.filter(status='pending').count()


            context = {
                'applied_jobs': applied_jobs,
                'application_count': application_count,
                'interviews_count': interviews_count,
                'offers_count': offers_count,
                'pending_count': pending_count,
            }
            return render(request, 'seeker_dashboard.html', context)
        elif request.user.user_type == 'recruiter':
            jobs = Job.objects.filter(recruiter=request.user)

            active_jobs = jobs.filter(application_deadline__gte=timezone.now())

            for job in active_jobs:
                job.skill_list = [s.strip() for s in (job.skills or '').split(',')]

            recent_applications = Application.objects.filter(job__in=jobs).order_by('-applied_at')[:5]
            for app in recent_applications:

                if hasattr(app.seeker, 'seeker_profile') and app.seeker.seeker_profile.skills:
                    app.skill_list = [s.strip() for s in app.seeker.seeker_profile.skills.split(',')]
                else:
                    app.skill_list = []

            job_count = active_jobs.count()
            application_count = Application.objects.filter(job__in=jobs).count()
            interviews_count = Application.objects.filter(job__in=jobs, status='interviewed').count()
            opp_count = Application.objects.filter(job__in=jobs, status='offered').count()

            context = {
                'jobs': jobs,
                'active_jobs': active_jobs,
                'recent_applications': recent_applications,
                'job_count': job_count,
                'application_count': application_count,
                'interviews_count': interviews_count,
                'opp_count': opp_count,
            }
            return render(request, 'recruiter_dashboard.html', context)
        



def job_list(request):
    jobs_count = Job.objects.filter(application_deadline__gte=timezone.now()).count()
    jobs = Job.objects.filter(application_deadline__gte=timezone.now())

    search_query = request.GET.get('search', '').strip()
    location_query = request.GET.get('location', '').strip()
    job_type_query = request.GET.get('job_type', '').strip()

    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(recruiter__recruiter_profile__company_name__icontains=search_query)
        )
    if location_query:
        jobs = jobs.filter(location__icontains=location_query)
    if job_type_query:
        jobs = jobs.filter(job_type__iexact=job_type_query)

    if request.user.is_authenticated:
        if request.user.user_type == 'job_seeker':
            seeker_skills = getattr(request.user.seeker_profile, 'skills', '') or ''
            seeker_skill_set = set([s.strip().lower() for s in seeker_skills.split(',') if s.strip()])
            for job in jobs:
                job_skill_list = [s.strip() for s in (job.skills or '').split(',') if s.strip()]
                job.skill_list = job_skill_list
                job_skill_set = set([s.lower() for s in job_skill_list])
                job.match_percentage = int((len(seeker_skill_set & job_skill_set) / len(job_skill_set)) * 100) if job_skill_set else 0
        elif request.user.user_type == 'recruiter':
            jobs = jobs.filter(recruiter=request.user)
            for job in jobs:
                job.skill_list = [s.strip() for s in (job.skills or '').split(',') if s.strip()]
    else:

        for job in jobs:
            job.skill_list = [s.strip() for s in (job.skills or '').split(',') if s.strip()]
            job.match_percentage = None  # No match shown

    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'joblist.html', {
        'jobs': page_obj,
        'jobs_count': jobs_count,
        'search_query': search_query,
        'location_query': location_query,
        'job_type_query': job_type_query
    })



def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm()
    return render(request, 'add_job.html', {'form': form})

def job_detail(request, job_id):

    job = get_object_or_404(Job, id=job_id, application_deadline__gte=timezone.now())
    job.skill_list = [s.strip() for s in (job.skills or '').split(',')]

    context = {
        'job': job
    }
    return render(request, 'jobdetails.html', context)
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter', '').strip()
        if Application.objects.filter(job=job, seeker=request.user).exists():
            messages.warning(request, 'You have already applied for this job.')
        else:
            Application.objects.create(
                job=job,
                seeker=request.user,
                cover_letter=cover_letter
            )
            messages.success(request, 'Your application has been submitted!')

    return redirect('job_list')
def withdraw_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, seeker=request.user)
    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Your application has been withdrawn.')
    return redirect('dashboard')

def update_application_status(request, id):
    application = get_object_or_404(Application, id=id)

    if request.method == 'POST':
            if application.status == 'pending':
                application.status = 'reviewed'
            elif application.status == 'reviewed':
                application.status = 'interviewed'
            elif application.status == 'interviewed':
                application.status = 'offered'
            else:
                messages.info(request, 'Cannot move to next status.')
                return redirect('dashboard')
            application.save()
            messages.success(request, f'Status updated to {application.get_status_display()}.')
    return redirect('dashboard')
def reject_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if request.method == 'POST':
        application.status = 'rejected'
        application.save()
        messages.success(request, 'Application has been rejected.')
    return redirect('dashboard')






def skill_match_view(request):
    if request.user.user_type == 'job_seeker':
        # Job Seeker: show matched jobs
        seeker_skills = getattr(request.user.seeker_profile, 'skills', '') or ''
        seeker_skill_set = set([s.strip().lower() for s in seeker_skills.split(',')])

        jobs = Job.objects.filter(application_deadline__gte=timezone.now())
        matched_jobs = []

        for job in jobs:
            job_skill_list = [s.strip() for s in (job.skills or '').split(',')]
            job.skill_list = job_skill_list

            job_skill_set = set([s.lower() for s in job_skill_list])
            if job_skill_set:
                match_count = len(seeker_skill_set & job_skill_set)
                match_percentage = int((match_count / len(job_skill_set)) * 100)
            else:
                match_percentage = 0

            if match_percentage > 0:
                job.match_percentage = match_percentage
                matched_jobs.append(job)

        matched_jobs.sort(key=lambda x: x.match_percentage, reverse=True)

        paginator = Paginator(matched_jobs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'user_type': 'job_seeker',
            'jobs': page_obj,
        }

    elif request.user.user_type == 'recruiter':
        jobs = Job.objects.filter(recruiter=request.user, application_deadline__gte=timezone.now())

        for job in jobs:
            job.skill_list = [s.strip() for s in (job.skills or '').split(',')]
            job.skill_set = set([s.lower() for s in job.skill_list])

            applications = job.applications.all()
            for app in applications:
                if hasattr(app.seeker, 'seeker_profile'):
                    seeker_skills = getattr(app.seeker.seeker_profile, 'skills', '') or ''
                    seeker_skill_set = set([s.strip().lower() for s in seeker_skills.split(',')])
                    match_count = len(job.skill_set & seeker_skill_set)
                    app.match_percentage = int((match_count / len(job.skill_set)) * 100) if job.skill_set else 0
                    app.match_skills = list(job.skill_set & seeker_skill_set)
                else:
                    app.match_percentage = 0
                    app.match_skills = []
            job.applications_with_match = applications

        context = {
            'user_type': 'recruiter',
            'jobs': jobs,
        }

    else:
        messages.error(request, 'Access denied.')
        return redirect('home')

    return render(request, 'skillmatch.html', context)
