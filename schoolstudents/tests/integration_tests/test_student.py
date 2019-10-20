import decimal
from datetime import date

from django.urls import reverse
from factory import fuzzy
from rest_framework import status
from rest_framework.test import APITestCase

from schoolstudents.models import Student
from schoolstudents.tests.factories import SchoolFactory, StudentFactory


class StudentAPITestCase(APITestCase):
    def test_create_student(self):
        school = SchoolFactory()
        data = {
            'first_name': 'John',
            'last_name': 'Cena',
            'age': '5.0',
            'school': school.id,
            'nationality': fuzzy.FuzzyText(length=10),
        }
        url = reverse('schoolstudents:students-list')
        response = self.client.post(url, data)
        student = Student.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertIsNotNone(student)
        self.assertEqual(student.first_name, data['first_name'])
        self.assertEqual(student.last_name, data['last_name'])
        self.assertEqual(student.age, decimal.Decimal(data['age']))
        self.assertEqual(student.school, school)
        self.assertEqual(str(student.nationality), str(data['nationality']))

    def test_update_student(self):
        new_school = SchoolFactory()
        student = StudentFactory(first_name='John', last_name='Cena', age=6.4)
        data = {
            'first_name': 'John',
            'last_name': 'Wick',
            'age': 6.40,
            'school': new_school.pk,
            'nationality': 'Bangladesh',
        }
        url = reverse('schoolstudents:students-detail', args=[student.pk])
        response = self.client.put(url, data)
        student.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(student.first_name, data['first_name'])
        self.assertEqual(student.last_name, data['last_name'])
        self.assertIsInstance(student.age, decimal.Decimal)
        self.assertEqual(student.school, new_school)
        self.assertEqual(student.nationality, 'Bangladesh')

    def test_partial_update_student(self):
        student = StudentFactory(first_name='John', last_name='Cena')
        identification = student.student_id
        first_name = student.first_name
        school = student.school

        data = {
            'last_name': 'Wick',
        }
        url = reverse('schoolstudents:students-detail', args=[student.pk])
        response = self.client.patch(url, data)
        student.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(student.last_name, data['last_name'])
        self.assertEqual(student.first_name, first_name)
        self.assertEqual(student.school, school)
        self.assertEqual(student.student_id, identification)

    def test_delete_student(self):
        student = StudentFactory()
        url = reverse('schoolstudents:students-detail', args=[student.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertEqual(Student.objects.count(), 0)

    def test_create_fail_due_to_maximum_student(self):
        school = SchoolFactory(max_students=1)
        StudentFactory(school=school)

        data = {
            'first_name': 'John',
            'last_name': 'Wick',
            'school': school.id,
            'nationality': fuzzy.FuzzyText(),
        }
        url = reverse('schoolstudents:students-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(str(response.data[0]), f'Maximum students limit exceeded for {school}.')

    def test_update_fail_due_to_maximum_student(self):
        school = SchoolFactory(max_students=1)
        StudentFactory(school=school)
        student = StudentFactory()
        data = {
            'school': school.id,
        }
        url = reverse('schoolstudents:students-detail', args=[student.pk])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(str(response.data[0]), f'Maximum students limit exceeded for {school}.')

    def test_retrieve_should_has_age_field(self):
        student = StudentFactory(first_name='John', last_name='Cena')
        url = reverse('schoolstudents:students-detail', args=[student.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIn('age', response.data.keys())