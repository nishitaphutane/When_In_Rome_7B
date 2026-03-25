from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

#model to store information about cities

class City(models.Model):
    name = models.CharField(max_length=128, unique=True)
    country = models.CharField(max_length=128, default='Unknown')
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name

#model for recommendations to visit places 
class Recommendation(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=256, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Recommendation, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def upvote_count(self):
        return self.upvote_set.count()

#model to store user profiles, including bio, profile picture, and followers and each follower is a normal Django User.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    pronouns = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    is_verified = models.BooleanField(default=False)
    followers = models.ManyToManyField(
        User,
        blank=True,
        related_name='following_profiles'
    )

    def __str__(self):
        return self.user.username
    
class VisitedCity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visited_cities')
    city_name = models.CharField(max_length=128)
    country_flag = models.CharField(max_length=10, blank=True)  # e.g. "🇬🇧"

    def __str__(self):
        return f"{self.user.username} visited {self.city_name}"

#model to store reviews and ratings for recommendations
class Review(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.recommendation.title} - {self.rating}"
    
#model to let users upvote recommendations
class Upvote(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} upvoted {self.recommendation.title}"
