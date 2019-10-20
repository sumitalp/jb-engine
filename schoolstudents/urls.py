from django.urls import path, include

from rest_framework_nested import routers

from schoolstudents import views

router = routers.DefaultRouter()
router.register(r'schools', views.SchoolModelViewSet, basename='schools')
router.register(r'students', views.StudentModelViewSet, basename='students')

nested_router = routers.NestedSimpleRouter(router, r'schools', lookup='school')
nested_router.register(r'students', views.StudentModelViewSet, basename='school-students')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls))
]