from django.test import TestCase
from feed.models import Friend
import uuid
# Create your tests here.

class AuthorTestCase(TestCase):
	follower = uuid.uuid4()
	followed = uuid.uuid4()

	def setup(self):
		Friend.objects.create(follower_id=self.follower, followed_id=self.followed)

	def test_check_values(self):
		friend = Friend.objects.get(follower_id=self.follower)
		friend_followed_id = friend.follower_id
		self.assertEqual(self.followed, friend_followed_id)
