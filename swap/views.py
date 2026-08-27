from django.shortcuts import render, redirect
from .models import UserProfile, SkillRequest


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


def reciprocal_matches(request):
    profiles = UserProfile.objects.all()

    matches = []

    for person in profiles:
        for teacher in profiles:

            if person.id == teacher.id:
                continue

            wanted = person.learning_skills.lower().strip()
            teaching = teacher.skills.lower().strip()

            if wanted and teaching and wanted in teaching:
                matches.append({
                    "learner": person,
                    "teacher": teacher,
                    "skill": wanted
                })

    return render(
        request,
        "swap/reciprocal_matches.html",
        {"matches": matches}
    )


def send_request(request, receiver_id):
    receiver = UserProfile.objects.get(id=receiver_id)

    if request.method == 'POST':
        skill = request.POST.get('skill')
        message = request.POST.get('message')

        sender = UserProfile.objects.first()

        SkillRequest.objects.create(
            sender=sender,
            receiver=receiver,
            skill=skill,
            message=message
        )

        return redirect('home')

    return render(
        request,
        'swap/send_request.html',
        {'receiver': receiver}
    )