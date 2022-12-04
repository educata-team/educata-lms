import json

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from jwt import decode

from backend import settings

from .permissions import *
from .serializers import *


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CreateUpdateDeletePermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if self.request.user.is_anonymous:
                return Response({'detail: You must be authorized'}, status.HTTP_401_UNAUTHORIZED)
            if self.request.user.role == 'lecturer':
                response = serializer.save()
                return Response(data=response, status=status.HTTP_201_CREATED)
            return Response({'detail': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        response = super(CourseViewSet, self).retrieve(request, *args, **kwargs)
        access_token = request.META.get('HTTP_AUTHORIZATION')
        print(access_token[7::])
        token = decode(access_token[7::], settings.SECRET_KEY, algorithms=['HS256'])
        print(token)
        return response


class CategoryViewsSet(ModelViewSet):
    permission_classes = [CreateUpdateDeletePermission]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def update(self, request, *args, **kwargs):
        return super(CategoryViewsSet, self).update(request, *args, **kwargs)


class UnitViewSet(ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class AttendedCourseViewSet(ModelViewSet):
    queryset = AttendedCourse.objects.all()
    serializer_class = AttendedCourseSerializer
    permission_classes = [AttendedCoursePermission]

    def get_object(self):
        try:
            return AttendedCourse.objects.get(course__pk=self.kwargs['pk'], user=self.request.user)
        except AttendedCourse.DoesNotExist:
            return None

    def get_queryset(self):
        return AttendedCourse.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            course = AttendedCourse.objects.get(course__pk=self.kwargs['pk'], user=self.request.user)
            serializer = self.get_serializer(course)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except (AttendedCourse.DoesNotExist, ValueError):
            return Response({'detail': 'You do not subscribed on requested course'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        print(request.data.get('id'))
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            print(serializer.data)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        object_to_delete = self.get_object()
        try:
            object_to_delete.delete()
        except AttributeError:
            return Response(data={'detail': 'Requesting course was not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'detail': 'Successfully deleted'}, status=status.HTTP_200_OK)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPermission]

    def get_queryset(self):
        try:
            reviews = Review.objects.select_related('user').filter(course__pk=self.kwargs['course_pk']).order_by('-created_at')
            return reviews
        except (ValueError, Review.DoesNotExist):
            return None

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(data=serializer.data)
        except (ValueError, AttributeError):
            return Response({'detail': 'Something went wrong. Check credentials'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            course = Course.objects.get(pk=self.kwargs.get('course_pk'))
        except (Course.DoesNotExist, ValidationError):
            return Response({'detail': 'Indicated course does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data, context={'user': request.user, 'course': course})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            course = Course.objects.get(pk=self.kwargs.get('course_pk'))
            review_to_delete = Review.objects.get(pk=self.kwargs['review_pk'], course=course, user=request.user)
            review_to_delete.delete()
            return Response({'detail': 'Successfully deleted'}, status=status.HTTP_200_OK)
        except (Course.DoesNotExist, ValidationError, Review.DoesNotExist):
            return Response({'detail': 'Indicated course or review does not exist'}, status=status.HTTP_404_NOT_FOUND)


class AssignmentModelViewSet(ModelViewSet):
    serializer_class = AssignmentSerializer

