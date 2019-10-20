import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class School(models.Model):
    name = models.CharField(max_length=20)
    max_students = models.PositiveIntegerField(default=20)
    city = models.CharField(max_length=80)
    country = models.CharField(max_length=80)
    address = models.TextField(blank=True)

    def __str__(self)->str:
        return self.name

    @property
    def total_student(self)->int:
        return self.students.count()


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    student_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    age = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    nationality = models.CharField(max_length=80)
    address = models.TextField(blank=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self)->str:
        return self.full_name
