from django.core.exceptions import ValidationError
from schoolstudents.models import School

def before_save_trigger_school(school_instance, student_limit, **kwargs):
    if school_instance.total_student > student_limit:
        return False
    return True