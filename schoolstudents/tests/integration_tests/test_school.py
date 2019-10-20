from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from schoolstudents.tests.factories import SchoolFactory, StudentFactory
from schoolstudents.models import School


class SchoolAPITestCase(APITestCase):
    def test_create_school(self):
        url = reverse('schoolstudents:schools-list')
        data = {
            'name': 'school1',
            'max_students': 10,
            'city': 'Dhaka',
            'country': 'Bangladesh'
        }
        response = self.client.post(url, data)
        school = School.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertIsNotNone(school)
        self.assertEqual(school.name, data['name'])
        self.assertEqual(school.max_students, data['max_students'])

    def test_update_school(self):
        school = SchoolFactory(name='school1', max_students=5, city='Dhaka', country='Bangladesh')
        url = reverse('schoolstudents:schools-detail', args=[school.pk])
        data = {
            'name': 'school2',
            'max_students': 20,
            'city': 'Dhaka',
            'country': 'Bangladesh'
        }
        response = self.client.put(url, data)
        school.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(school.name, data['name'])
        self.assertEqual(school.max_students, data['max_students'])

    def test_partial_update_school(self):
        school = SchoolFactory(max_students=5, city='Chittagong', country='Bangladesh')
        name = school.name
        url = reverse('schoolstudents:schools-detail', args=[school.pk])
        data = {
            'max_students': 20,
        }
        response = self.client.patch(url, data)
        school.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(school.name, name)
        self.assertEqual(school.max_students, data['max_students'])

    def test_delete_school(self):
        school = SchoolFactory()
        url = reverse('schoolstudents:schools-detail', args=[school.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertEqual(School.objects.count(), 0)

    # def test_update_fail_due_to_maximum_student(self):
    #     school = SchoolFactory(name='school1', max_students=2)
    #     StudentFactory(school=school)
    #     StudentFactory(school=school)
    #     url = reverse('schoolstudents:schools-detail', args=[school.pk])
    #     data = {
    #         'max_students': 1,
    #     }
    #     response = self.client.patch(url, data)
    #     school.refresh_from_db()
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
    #     self.assertEqual(response.data, {'max_students': ['The number of students exceeds the maximum students']})