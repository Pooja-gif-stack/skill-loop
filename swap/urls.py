from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create-profile/", views.create_profile, name="create_profile"),
    path("reciprocal/", views.reciprocal_matches, name="reciprocal_matches"),
    path("send-request/<int:receiver_id>/", views.send_request, name="send_request"),
]