from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid
from .utils.bayesian_ratings import calculate_bayesian_average
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    developer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255)
    description = models.TextField()
    source_code_url = models.URLField(max_length=500)
    demo_url = models.URLField(max_length=500, blank=True, null=True)
    live_url = models.URLField(max_length=500, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    ratings = models.ManyToManyField('Rating', related_name='projects', blank=True)
    average_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="projects", db_index=True)
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)    
    views_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)    

    def update_average_rating(self):
        """Method to update the average rating of the project using Bayesian average."""
        self.average_rating = calculate_bayesian_average(self)
        self.save()

    def __str__(self):

        return self.title

class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_ratings")
    consumer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'consumer')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the rating
        self.project.update_average_rating()  # Update the project's average rating

    def __str__(self):
        return f"{self.consumer.username} rated {self.project.title} - {self.rating} (Comment: {self.comment})"
