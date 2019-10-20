import os
import random
from faker import Faker

# Set Django Module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manatal_challenge.settings')

import django
django.setup()

from django.core.exceptions import ValidationError
from schoolstudents.models import School, Student


fake_generator = Faker()
schools = ["St. Gregory's School", "St. Joseph School", "Scholastica School",
    "Green Herald School", "St. Francis School", "Ideal Boys School"
]

def create_school() -> School:
    """
    Create school with fake data
    """
    school, created = School.objects.get_or_create(
        name=random.choice(schools),
        defaults={
            "city": fake_generator.city(),
            "country": fake_generator.country(),
            "max_students": random.randint(5,20),
            "address": fake_generator.address()
        }
    )

    return school

def populate(iterations=100):
    for entry in range(iterations):

        school = create_school()

        try:
            Student.objects.get_or_create(
                first_name=fake_generator.first_name(), 
                last_name=fake_generator.last_name(),
                defaults={
                    'address': fake_generator.address(),
                    'age': round(random.uniform(4,15.5), 1),
                    'nationality': fake_generator.country(),
                    'school': school
                }
            )
        except ValidationError as ex:
            print(ex)


if __name__ == '__main__':
    print('Started: Data population')
    populate(iterations=100)
    print('End')