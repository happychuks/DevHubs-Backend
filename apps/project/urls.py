from django.urls import path
from .views import ProjectListView, ProjectDetailView, CategoryListView, TagListView, ProjectRatingView, ProjectSearchView

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<uuid:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/categories/', CategoryListView.as_view(), name='category-list'),
    path('projects/tags/', TagListView.as_view(), name='tag-list'),
    path('projects/<uuid:pk>/rate/', ProjectRatingView.as_view(), name='project-rate'),
    path('projects/search/', ProjectSearchView.as_view(), name='project-search'),
]
