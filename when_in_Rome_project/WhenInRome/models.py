from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class City(models.Model):
    name = models.CharField(max_length=128, unique=True)
    country = models.CharField(max_length=128, default='Unknown')
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def save(self, args, **kwargs):
        self.slug = slugify(self.name)
        super(City, self).save(args, **kwargs)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name

class Recommendation(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=256, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, args, **kwargs):
        self.slug = slugify(self.title)
        super(Recommendation, self).save(args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
class Review(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.recommendation.title} - {self.rating}"