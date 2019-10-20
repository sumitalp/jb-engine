from django.core.exceptions import ValidationError
from schoolstudents.models import School

def before_save_trigger_student(school_obj, **kwargs):
    if school_obj.total_student >= school_obj.max_students:
        return False
    return True