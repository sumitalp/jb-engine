from django.db import transaction
from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError

from schoolstudents.models import School, Student
from schoolstudents.serializers import SchoolSerializer, StudentSerializer
from schoolstudents.services.school_validation import before_save_trigger_school
from schoolstudents.services.student_validation import before_save_trigger_student


class SchoolModelViewSet(viewsets.ModelViewSet):
    """
    ## School Management
    -----------------------
    - List API 
        1. Method: **GET**
        2. URL: api/schools/
    - Search
        1. Method: **GET**
        2. URL: api/schools/?serach=school
    - Create School 
        1. Method: **POST**
        2. URL: api/schools/
        3. Request Parameters
            - name: name
                - type: string
                - **required: true**
                - desc: Maximum 20 characters length
            - name: max_students
                - type: integer
                - **required: true**
                - desc: Maximum students limit in school
            - name: address
                - type: string
            - name: city
                - type: string
                - **required: true**
                - desc: Maximum 80 characters length
            - name: country
                - type: string
                - **required: true**
                - desc: Maximum 80 characters length
    - School detail
        1. Method: **GET**
        2. URL: api/schools/{pk}/
        3. `pk`
            - type: interger
            - description: It should be school id.
    - School update
        1. Method: **PUT**
        2. URL: api/schools/{pk}/
        3. `pk`
            - type: interger
            - description: It should be school id.
    - School partial update
        1. Method: **PATCH**
        2. URL: api/schools/{pk}/
        3. `pk`
            - type: interger
            - description: It should be school id.
    """
    serializer_class = SchoolSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('name', 'max_students')
    ordering_fields = ('name', 'city', 'country', )
    queryset = School.objects.all()

    def update(self, request, *args, **kwargs):
        """
        Check maximum students limit and then save.
        """
        max_students = request.data.get('max_students', None)
        school_obj = self.get_object()
        if max_students and not before_save_trigger_school(school_obj, int(max_students)):
            raise ValidationError(f'Maximum students limit exceeded for {school_obj}.')
        with transaction.atomic():
            return super().update(request, *args, **kwargs)


class StudentModelViewSet(viewsets.ModelViewSet):
    """
    ## Student Management
    -----------------------
    - List API 
        1. Method: **GET**
        2. URL: 
            - api/students/
            - api/schools/{school_pk}/students/
    - Search
        1. Method: **GET**
        2. URL: 
            - api/students/?serach=ahsan
            - api/schools/{school_pk}/students/?serach=ahsan
    - Create Student 
        1. Method: **POST**
        2. URL: 
            - api/students/
            - api/schools/{school_pk}/students/
        3. Request Parameters
            - name: first_name
                - type: string
                - **required: true**
                - desc: Maximum 64 characters length
            - name: last_name
                - type: string
                - **required: true**
                - desc: Maximum 64 characters length
            - name: address
                - type: string
            - name: nationality
                - type: string
                - **required: true**
                - desc: Maximum 80 characters length
            - name: age
                - type: float
                - **required: true**
                - desc: float bype because try to keep both year and month
            - name: school
                - type: integer
                - **required: true**
                - desc: School type object
    - Student detail
        1. Method: **GET**
        2. URL: 
            - api/students/{pk}/
            - api/schools/{school_pk}/students/{pk}/
        3. `pk`
            - type: interger
            - description: It should be student id.
    - Student update
        1. Method: **PUT**
        2. URL: 
            - api/students/{pk}/
            - api/schools/{school_pk}/students/{pk}/
        3. `pk`
            - type: interger
            - description: It should be student id.
    - Student partial update
        1. Method: **PATCH**
        2. URL: 
            - api/students/{pk}/
            - api/schools/{school_pk}/students/{pk}/
        3. `pk`
            - type: interger
            - description: It should be student id.
    """
    serializer_class = StudentSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('first_name', 'last_name', )
    ordering_fields = (
        'first_name', 'last_name',
        'age', 'nationality', 
        'school__name', 'school__city', 'school_country', 
        )
    queryset = Student.objects.all()

    def get_queryset(self):
        """
        Filter queryset if school_pk exists, otherwise return all
        """
        queryset = self.queryset
        school_pk = self.kwargs.get('school_pk', None)

        if school_pk:
            queryset = queryset.filter(school=school_pk)

        return queryset

    def perform_create(self, serializer):
        """
        Prevent concurrent save and maximum students limit in school.
        """
        with transaction.atomic():
            school = serializer.validated_data.get('school', None)
            if school and not before_save_trigger_student(school):
                raise ValidationError(f'Maximum students limit exceeded for {school}.')
                
            serializer.save()

    def perform_update(self, serializer):
        """
        Prevent concurrent save and maximum students limit in school.
        """
        with transaction.atomic():
            school = serializer.validated_data.get('school', None)
            if school and not before_save_trigger_student(school):
                raise ValidationError(f'Maximum students limit exceeded for {school}.')
                
            serializer.save()

