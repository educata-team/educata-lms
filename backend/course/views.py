from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView

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
        return response


class CategoryViewsSet(ModelViewSet):
    permission_classes = [CreateUpdateDeletePermission]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def update(self, request, *args, **kwargs):
        return super(CategoryViewsSet, self).update(request, *args, **kwargs)


class UnitListCreateAPIView(ListCreateAPIView, DestroyAPIView):
    serializer_class = UnitSerializer
    lookup_field = 'unit_pk'
    permission_classes = [UnitPermission]

    def get_queryset(self):
        return Unit.objects.select_related('course').filter(course=Course.objects.get(pk=self.kwargs.get('course_pk')))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            course = Course.objects.get(pk=self.kwargs.get('course_pk'))
        except Course.DoesNotExist:
            return Response(data={'detail': 'Couse does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data, context={'course': course})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            unit_to_delete = Unit.objects.get(pk=request.data.get('unit_pk'))
            self.check_object_permissions(self.request, obj=unit_to_delete)
            unit_to_delete.delete()
            return Response(data={'detail': 'Successfully deleted'}, status=status.HTTP_200_OK)
        except Unit.DoesNotExist:
            return Response(data={'detail': 'Indicated unit does not exist'}, status=status.HTTP_404_NOT_FOUND)


class UnitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UnitSerializer
    lookup_field = 'unit_pk'
    permission_classes = [UnitPermission]

    def get_object(self):
        try:
            unit = Unit.objects.select_related('course').get(pk=self.kwargs.get('unit_pk'),
                                                             course=Course.objects.get(pk=self.kwargs.get('course_pk')))
            return unit
        except (Unit.DoesNotExist, Course.DoesNotExist):
            return None

    def retrieve(self, request, *args, **kwargs):
        unit = self.get_object()
        if not unit:
            return Response(data={'detail': 'Unit or course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance=unit)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        unit = self.get_object()
        self.check_object_permissions(self.request, obj=unit)
        if not unit:
            return Response(data={'detail': 'Indicated unit does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data, instance=unit)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
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


class AssignmentListCreateAPIView(ListCreateAPIView):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        try:
            return Assignment.objects.select_related('unit__course').filter(unit__course__pk=self.kwargs.get('course_pk'))
        except (KeyError, AttributeError):
            return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            unit = Unit.objects.select_related('course', 'course__owner').get(pk=request.data.get('unit'), course__isnull=False)
        except Unit.DoesNotExist:
            return Response(data='Indicated unit does not exist', status=status.HTTP_404_NOT_FOUND)

        if request.user != unit.course.owner:
            return Response({'detail': 'You do not have permission to create assignment for this course'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data, context={'unit': unit})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={'detail': 'Errors occures'}, status=status.HTTP_400_BAD_REQUEST)
