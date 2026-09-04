from django.test import TestCase, Client
from django.urls import reverse
from .models import UserProfile, SkillRequest, MentorBooking


class SwapUnifiedEndpointTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = UserProfile.objects.create(
            name="Alice",
            email="alice@example.com",
            phone="1234567890",
            bio="Python developer",
            skills="Python, Django",
            learning_skills="React"
        )
        self.user2 = UserProfile.objects.create(
            name="Bob",
            email="bob@example.com",
            phone="0987654321",
            bio="Frontend developer",
            skills="React, JavaScript",
            learning_skills="Python"
        )

    def test_single_endpoint_get_dashboard(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('matches', response.context)
        self.assertIn('profiles', response.context)
        self.assertIn('all_requests', response.context)
        self.assertIn('all_bookings', response.context)
        self.assertEqual(response.context['total_profiles_count'], 2)

    def test_single_endpoint_create_profile(self):
        response = self.client.post(reverse('home'), {
            'action': 'create_profile',
            'name': 'David',
            'email': 'david@example.com',
            'phone': '9988776655',
            'bio': 'Cloud Architect',
            'skills': 'AWS, Docker',
            'learning_skills': 'Kubernetes'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserProfile.objects.filter(email='david@example.com').exists())

    def test_single_endpoint_switch_user_and_login(self):
        response = self.client.post(reverse('home'), {
            'action': 'switch_user',
            'user_id': self.user2.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['user_id'], self.user2.id)

        response = self.client.post(reverse('home'), {
            'action': 'login',
            'email': 'alice@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['user_id'], self.user1.id)

    def test_single_endpoint_send_request(self):
        response = self.client.post(reverse('home'), {
            'action': 'send_request',
            'sender_id': self.user1.id,
            'receiver_id': self.user2.id,
            'skill': 'React',
            'message': 'Let us trade skills!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            SkillRequest.objects.filter(sender=self.user1, receiver=self.user2, skill='React').exists()
        )

    def test_single_endpoint_update_request_status(self):
        req = SkillRequest.objects.create(
            sender=self.user1,
            receiver=self.user2,
            skill='React',
            message='Swap proposal',
            status='Pending'
        )
        response = self.client.post(reverse('home'), {
            'action': 'update_request',
            'request_id': req.id,
            'status': 'Accepted'
        })
        self.assertEqual(response.status_code, 302)
        req.refresh_from_db()
        self.assertEqual(req.status, 'Accepted')

    def test_single_endpoint_book_mentor(self):
        response = self.client.post(reverse('home'), {
            'action': 'book_mentor',
            'student_id': self.user1.id,
            'mentor_id': self.user2.id,
            'date': '2026-09-01',
            'time': '10:00:00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            MentorBooking.objects.filter(student=self.user1, mentor=self.user2).exists()
        )

    def test_compatibility_standalone_endpoints(self):
        # Create profile endpoint
        res = self.client.get(reverse('create_profile'))
        self.assertEqual(res.status_code, 200)

        # Reciprocal matches endpoint
        res = self.client.get(reverse('reciprocal_matches'))
        self.assertEqual(res.status_code, 200)

        # Send request endpoint
        res = self.client.get(reverse('send_request', args=[self.user2.id]))
        self.assertEqual(res.status_code, 200)

        # Received requests endpoint
        res = self.client.get(reverse('received_requests'))
        self.assertEqual(res.status_code, 200)

        # Login endpoint
        res = self.client.get(reverse('login'))
        self.assertEqual(res.status_code, 200)

