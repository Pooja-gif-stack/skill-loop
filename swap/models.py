from django.db import models


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=500)
    learning_skills = models.CharField(max_length=500)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.name


class SkillRequest(models.Model):
    sender = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='sent_requests'
    )
    receiver = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='received_requests'
    )
    skill = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Accepted', 'Accepted'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.name} → {self.receiver.name}"


class MentorBooking(models.Model):
    student = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    mentor = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='mentor_bookings'
    )
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default='Booked')

    def __str__(self):
        return f"{self.student.name} booked {self.mentor.name}"