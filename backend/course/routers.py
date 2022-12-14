from rest_framework.routers import DefaultRouter
from course.views import *


router = DefaultRouter()
router.register(r'course', CourseViewSet)
router.register(r'category', CategoryViewsSet)
router.register(r'attended-course', AttendedCourseViewSet)
