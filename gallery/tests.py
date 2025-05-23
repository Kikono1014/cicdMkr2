from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Image, Category

class ImageModelViewTests(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='Nature')
        self.category2 = Category.objects.create(name='City')

        self.recent_image = Image.objects.create(
            title='New image',
            image='gallery_images/recent.jpg',
            created_date=timezone.now().date() - timedelta(days=10),
            age_limit=0
        )
        self.recent_image.categories.add(self.category1)

        self.old_image = Image.objects.create(
            title='Old image',
            image='gallery_images/old.jpg',
            created_date=timezone.now().date() - timedelta(days=40),
            age_limit=0
        )
        self.old_image.categories.add(self.category2)

    def test_image_str_representation(self):
        self.assertEqual(str(self.recent_image), 'New image')
        self.assertEqual(str(self.old_image), 'Old image')

    def test_category_str_representation(self):
        self.assertEqual(str(self.category1), 'Nature')
        self.assertEqual(str(self.category2), 'City')

    def test_gallery_view_displays_recent_images(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recent_image.title)
        self.assertNotContains(response, self.old_image.title)

    def test_image_detail_view(self):
        response = self.client.get(reverse('image_detail', args=[self.recent_image.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recent_image.title)

    def test_image_detail_view_nonexistent(self):
        response = self.client.get(reverse('image_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)
