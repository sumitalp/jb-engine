import factory
from factory import fuzzy
from schoolstudents.models import School, Student


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School

    name = fuzzy.FuzzyText(length=20)
    max_students = fuzzy.FuzzyInteger(1, 20)
    city = fuzzy.FuzzyText(length=60)
    country = fuzzy.FuzzyText(length=60)


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    first_name = fuzzy.FuzzyText(length=20)
    last_name = fuzzy.FuzzyText(length=20)
    age = fuzzy.FuzzyDecimal(5, high=20)
    address = fuzzy.FuzzyText(length=60)
    nationality = fuzzy.FuzzyText(length=60)
    school = factory.SubFactory(SchoolFactory)
