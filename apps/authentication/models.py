from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
import uuid

class User(AbstractUser):
    ROLE_CHOICES = (
        ('developer', 'Developer'),
        ('consumer', 'Consumer'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    roles = models.CharField(max_length=50, choices=ROLE_CHOICES, default='consumer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_developer(self):
        return self.roles == 'developer'

    def is_consumer(self):
        return self.roles == 'consumer'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    verified = models.BooleanField(default=False)

def create_user_profile(sender, instance, created, **kwargs):
    """Create a user profile when a new user is created."""
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
