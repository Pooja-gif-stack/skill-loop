from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    skills_to_teach = models.CharField(
        max_length=255,
        blank=True
    )

    skills_to_learn = models.CharField(
        max_length=255,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.user.username


class SkillRequest(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_requests"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_requests"
    )

    skill = models.CharField(
        max_length=100
    )

    message = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"


class MentorBooking(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="mentor_bookings"
    )

    mentor_name = models.CharField(
        max_length=100
    )

    skill = models.CharField(
        max_length=100
    )

    booking_date = models.DateField()

    booking_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    def __str__(self):
        return f"{self.student.username} - {self.mentor_name}"