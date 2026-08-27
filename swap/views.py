from django.shortcuts import render, redirect
from .models import UserProfile


def home(request):
    return render(request, 'swap/home.html')


def create_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        skills = request.POST.get('skills')
        learning_skills = request.POST.get('learning_skills')
        profile_image = request.FILES.get('profile_image')

        UserProfile.objects.create(
            name=name,
            email=email,
            phone=phone,
            bio=bio,
            skills=skills,
            learning_skills=learning_skills,
            profile_image=profile_image
        )

        return redirect('home')

    return render(request, 'swap/create_profile.html')