
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile/update/', update_profile, name='update_profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile_view, name='profile'),
    path('password_change/', password_change, name='password_change'),
    path('jobs/', job_list, name='job_list'),
    path('jobs/add/', add_job, name='add_job'),
    path('jobs/<int:job_id>/', job_detail, name='job_detail'),
    path('job/<int:job_id>/apply/', apply_job, name='apply_job'),
    path('job/<int:job_id>/withdraw/', withdraw_application, name='withdraw_application'),
    path('application/<int:id>/', update_application_status, name='update_application_status'),
    path('application/<int:id>/reject/', reject_application, name='reject_application'),
    path('skillmatch/', skill_match_view, name='skill_match'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
