from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Project, Category, Tag
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectAPITests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.developer = User.objects.create_user(
            username='devuser',
            email='devuser@example.com',
            password='password'
        )
        self.consumer = User.objects.create_user(
            username='consuser',
            email='consuser@example.com',
            password='password'
        )

        # Create a category and tag
        self.category = Category.objects.create(name='Utility')
        self.tag = Tag.objects.create(name='Productivity')

        # Login the developer
        self.client.login(username='devuser', password='password')

    def test_create_project(self):
        url = reverse('project-list')
        data = {
            'title': 'Test Project',
            'description': 'A test project description.',
            'source_code_url': 'https://github.com/test/project',
            'live_url': 'https://liveproject.com',
            'demo_url': 'https://demo.project.com',
            'is_paid': False,
            'price': 0,
            'category': self.category.id,
            'tags': [self.tag.id],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().title, 'Test Project')

    def test_retrieve_project(self):
        project = Project.objects.create(
            title='Test Project',
            description='A test project description.',
            source_code_url='https://github.com/test/project',
            live_url='https://liveproject.com',
            demo_url='https://demo.project.com',
            is_paid=False,
            price=0,
            developer=self.developer,
            category=self.category
        )
        url = reverse('project-detail', args=[project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Project')

    def test_update_project(self):
        project = Project.objects.create(
            title='Old Project Title',
            description='Old description.',
            source_code_url='https://github.com/test/project',
            live_url='https://liveproject.com',
            demo_url='https://demo.project.com',
            is_paid=False,
            price=0,
            developer=self.developer,
            category=self.category
        )
        url = reverse('project-detail', args=[project.id])
        data = {
            'title': 'Updated Project Title',
            'description': 'Updated description.',
            'source_code_url': 'https://github.com/test/updated_project',
            'live_url': 'https://updatedliveproject.com',
            'demo_url': 'https://updateddemo.project.com',
            'is_paid': True,
            'price': 10.00,
            'category': self.category.id,
            'tags': [self.tag.id],
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.get().title, 'Updated Project Title')

    def test_delete_project(self):
        project = Project.objects.create(
            title='Project to Delete',
            description='Description for deletion.',
            source_code_url='https://github.com/test/project',
            live_url='https://liveproject.com',
            demo_url='https://demo.project.com',
            is_paid=False,
            price=0,
            developer=self.developer,
            category=self.category
        )
        url = reverse('project-detail', args=[project.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

    def test_list_projects(self):
        Project.objects.create(
            title='Project 1',
            description='Description 1.',
            source_code_url='https://github.com/test/project1',
            live_url='https://liveproject1.com',
            demo_url='https://demo.project1.com',
            is_paid=False,
            price=0,
            developer=self.developer,
            category=self.category
        )
        Project.objects.create(
            title='Project 2',
            description='Description 2.',
            source_code_url='https://github.com/test/project2',
            live_url='https://liveproject2.com',
            demo_url='https://demo.project2.com',
            is_paid=True,
            price=9.99,
            developer=self.developer,
            category=self.category
        )
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_projects(self):
        project = Project.objects.create(
            title='Searchable Project',
            description='This project can be searched.',
            source_code_url='https://github.com/test/searchable_project',
            live_url='https://searchableproject.com',
            demo_url='https://demo.searchableproject.com',
            is_paid=False,
            price=0,
            developer=self.developer,
            category=self.category
        )
        url = reverse('project-list') + '?search=Searchable'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Searchable Project')

    def test_project_requires_authentication(self):
        self.client.logout()
        url = reverse('project-list')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # User must be authenticated

