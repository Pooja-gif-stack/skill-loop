from django.contrib import admin
from .models import UserProfile, SkillRequest, MentorBooking


admin.site.register(UserProfile)
admin.site.register(SkillRequest)
admin.site.register(MentorBooking)