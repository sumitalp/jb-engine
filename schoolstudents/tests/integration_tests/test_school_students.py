from faker import Faker
from django.urls import reverse
from factory import fuzzy
from rest_framework import status
from rest_framework.test import APITestCase

from schoolstudents.models import Student
from schoolstudents.tests.factories import SchoolFactory, StudentFactory


class SchoolStudentAPITestCase(APITestCase):
    def test_list_student_in_school(self):
        school1 = SchoolFactory(max_students=3)
        school2 = SchoolFactory(max_students=2)
        StudentFactory(school=school1)
        StudentFactory(school=school1)
        StudentFactory(school=school1)
        StudentFactory(school=school2)
        StudentFactory(school=school2)
        url = reverse('schoolstudents:school-students-list', kwargs={'school_pk': school1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertGreater(len(response.data['results']), 0)

        url = reverse('schoolstudents:school-students-list', kwargs={'school_pk': school2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertGreater(len(response.data['results']), 0)

    def test_list_student_in_school_fail_no_detail(self):
        school1 = SchoolFactory(max_students=1)
        StudentFactory(school=school1)
        student_from_another_school = StudentFactory()
        url = reverse('schoolstudents:school-students-detail', kwargs={
            'school_pk': school1.pk,
            'pk': student_from_another_school.pk,
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.data)

    def test_create_student_in_school(self):
        school = SchoolFactory()
        data = {
            'first_name': 'Hulk',
            'last_name': 'Hogan',
            'nationality': fuzzy.FuzzyText(length=10),
            'age': 4.0,
            'school': school.pk
        }
        url = reverse('schoolstudents:school-students-list', kwargs={'school_pk': school.pk})
        response = self.client.post(url, data)
        student = Student.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertIsNotNone(student)
        self.assertEqual(student.first_name, data['first_name'])
        self.assertEqual(student.last_name, data['last_name'])
        self.assertEqual(student.school, school)
        self.assertEqual(str(student.nationality), str(data['nationality']))
        self.assertNotEqual(student.student_id, '')

    def test_update_student_in_school(self):
        school = SchoolFactory()
        new_school = SchoolFactory()
        student = StudentFactory(school=school, first_name='John', last_name='Cena')
        data = {
            'first_name': 'John',
            'last_name': 'Wick',
            'school': new_school.pk,
            'nationality': fuzzy.FuzzyText(),
        }
        url = reverse('schoolstudents:school-students-detail', kwargs={
            'school_pk': school.pk,
            'pk': student.pk,
        })
        response = self.client.put(url, data)
        student = Student.objects.first()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIsNotNone(student)
        self.assertEqual(student.first_name, data['first_name'])
        self.assertEqual(student.last_name, data['last_name'])
        self.assertEqual(student.school, new_school)
        self.assertEqual(str(student.nationality), str(data['nationality']))

    def test_partial_update_student_in_school(self):
        school = SchoolFactory()
        new_school = SchoolFactory()
        student = StudentFactory(school=school, first_name='John', last_name='Cena')

        identification = student.student_id
        first_name = student.first_name
        last_name = student.last_name

        data = {
            'school': new_school.pk,
        }
        url = reverse('schoolstudents:school-students-detail', kwargs={
            'school_pk': school.pk,
            'pk': student.pk,
        })
        response = self.client.patch(url, data)
        student.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(student.first_name, first_name)
        self.assertEqual(student.last_name, last_name)
        self.assertEqual(student.school, new_school)
        self.assertEqual(student.student_id, identification)

    def test_delete_student_in_school(self):
        school = SchoolFactory()
        student = StudentFactory(school=school)
        url = reverse('schoolstudents:school-students-detail', kwargs={
            'school_pk': school.pk,
            'pk': student.pk,
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertEqual(Student.objects.count(), 0)

    def test_create_fail_due_to_maximum_student(self):
        school = SchoolFactory(max_students=1)
        nationality = fuzzy.FuzzyText()
        StudentFactory(school=school)

        data = {
            'first_name': 'John',
            'last_name': 'Wick',
            'nationality': nationality,
            'age': 3.5,
            'school': school.pk
        }
        url = reverse('schoolstudents:school-students-list', kwargs={'school_pk': school.pk})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(str(response.data[0]), f'Maximum students limit exceeded for {school}.')

    def test_update_fail_due_to_maximum_student(self):
        school1 = SchoolFactory(max_students=1)
        StudentFactory(school=school1)

        school2 = SchoolFactory()
        student2 = StudentFactory(school=school2)

        # Move the student2 from the school2 to the school1
        data = {
            'school': school1.id,
        }
        url = reverse('schoolstudents:school-students-detail', kwargs={
            'school_pk': school2.pk,
            'pk': student2.pk,
        })
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(str(response.data[0]), f'Maximum students limit exceeded for {school1}.')
