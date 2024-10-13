from rest_framework import serializers
from .models import Project, Category, Tag, Rating


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'project', 'consumer', 'rating', 'comment']

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value

class ProjectSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, required=False)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    developer = serializers.StringRelatedField()
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a positive number")
        return value

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'source_code_url', 'live_url',
            'demo_url', 'is_paid', 'price', 'developer', 'category', 'tags',
            'views_count', 'downloads_count', 'ratings', 'average_rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['average_rating', 'views_count', 'downloads_count']
    
    def create(self, validated_data):
        ratings_data = validated_data.pop('ratings', [])
        project = Project.objects.create(**validated_data)
        for rating_data in ratings_data:
            Rating.objects.create(project=project, **rating_data)
        return project



