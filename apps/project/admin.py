from django.contrib import admin
from .models import Project, Rating, Tag, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    ordering = ('name',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    ordering = ('name',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'developer', 'category', 'display_tags', 'is_paid', 'views_count', 'downloads_count', 'average_rating', 'created_at')
    search_fields = ('title', 'category', 'tags')
    ordering = ('-created_at','average_rating')
    list_filter = ('created_at', 'category', 'tags', 'is_paid', 'average_rating')

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    display_tags.short_description = 'Tags'

class RatingAdmin(admin.ModelAdmin):
    list_display = ('project', 'consumer', 'rating', 'created_at')
    search_fields = ('project__name', 'user__username', 'rating')
    ordering = ('-rating',)
    list_filter = ('rating', 'created_at')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Rating, RatingAdmin)