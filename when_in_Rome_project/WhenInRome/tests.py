from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from WhenInRome.models import City, Recommendation, Upvote,Review,UserProfile,User

# Create your tests here.

class UpvoteCountTest(TestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(username='testuser1', password='test123')
        self.user2 = User.objects.create_user(username='testuser2', password='test123')
        self.user3 = User.objects.create_user(username='testuser3', password='test123')

        self.city = City.objects.create(name='Glasgow', country='Scotland')

        self.recommendation = Recommendation.objects.create(
            city=self.city,
            user=self.user1,
            title='Kelvingrove Art Gallery',
            description='Great museum',
            location='Kelvingrove'
        )

    def test_upvote_count_is_zero_with_no_upvotes(self):
        self.assertEqual(self.recommendation.upvote_count, 0)

    def test_upvote_count_increases(self):
        Upvote.objects.create(recommendation=self.recommendation, user=self.user2)
        self.assertEqual(self.recommendation.upvote_count, 1)

    def test_upvote_count_with_multiple_upvotes(self):
        Upvote.objects.create(recommendation=self.recommendation, user=self.user2)
        Upvote.objects.create(recommendation=self.recommendation, user=self.user3)
        self.assertEqual(self.recommendation.upvote_count, 2)
    

class CityModelTest(TestCase):
     
    def setUp(self):
        self.city = City.objects.create(name="Glasgow", country='Scotland', description="People make Glasgow")

    def test_city_is_created_correctly(self):
        self.assertEqual(self.city.name, 'Glasgow')
        self.assertEqual(self.city.country, 'Scotland')
        self.assertEqual(self.city.description, 'People make Glasgow')

    def test_slug_is_correct_for_city(self):
        self.assertEqual(self.city.slug, 'glasgow')

    def test_duplicate_city_name_is_rejected(self):
        with self.assertRaises(IntegrityError):
            City.objects.create(name='Glasgow', country='Scotland')

class ReviewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='test123')
        self.user2 = User.objects.create_user(username='testuser2', password='test123')

        self.city = City.objects.create(name='Glasgow', country='Scotland')

        self.recommendation = Recommendation.objects.create(
            city=self.city,
            user=self.user1,
            title='Kelvingrove Art Gallery',
            description='Great museum',
            location='Kelvingrove'
        )

    def test_review_is_created_correctly(self):
        review = Review.objects.create(
            recommendation=self.recommendation,
            user=self.user2,
            rating=5,
            comment='Amazing place!'
        )
        self.assertEqual(review.recommendation, self.recommendation)
        self.assertEqual(review.user, self.user2)
        self.assertEqual(review.comment, 'Amazing place!')

    def test_rating_is_saved_correctly(self):
        review = Review.objects.create(
            recommendation=self.recommendation,
            user=self.user2,
            rating=4,
            comment='Really good!'
        )
        self.assertEqual(review.rating, 4)

    def test_str_representation(self):
        review = Review.objects.create(
            recommendation=self.recommendation,
            user=self.user2,
            rating=5,
            comment='Amazing place!'
        )
        self.assertEqual(str(review), 'testuser2 - Kelvingrove Art Gallery - 5')

class UserProfileTest(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='test123')
        self.user2 = User.objects.create_user(username='testuser2', password='test123')

        self.profile1 = UserProfile.objects.create(user=self.user1, bio='Hi I am testuser1')
        self.profile2 = UserProfile.objects.create(user=self.user2, bio='Hi I am testuser2')

    def test_profile_is_created_correctly(self):
        self.assertEqual(self.profile1.user, self.user1)
        self.assertEqual(self.profile1.bio, 'Hi I am testuser1')
    
    def test_follow_feature_working_correctly(self):
        self.profile1.followers.add(self.user2)
        self.assertIn(self.user2, self.profile1.followers.all())
    
    def test_unfollow_feature_working_correctly(self):
        self.profile1.followers.add(self.user2)
        self.profile1.followers.remove(self.user2)
        self.assertNotIn(self.user2, self.profile1.followers.all())