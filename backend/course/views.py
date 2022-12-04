from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, \
    RetrieveUpdateAPIView

from .permissions import *
from .serializers import *


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CreateUpdateDeletePermission]

    def get_object(self):
        try:
            course = Course.objects.get(pk=self.kwargs.get('pk'))
            self.check_object_permissions(self.request, course)
            return course
        except Course.DoesNotExist:
            return None

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        serializer = self.get_serializer(data=request.data, context={'owner': request.user})
        if serializer.is_valid():
            serializer.save()
            response = serializer.data
            del response['category']
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj:
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'Indicated course does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj:
            return Response({'detail': 'Indicated course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data, instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj:
            return Response({'detail': 'Indicated course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response({'detail': 'Successfully deleted'}, status=status.HTTP_200_OK)


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
            unit_to_delete = Unit.objects.get(pk=request.data.get('unit_id'))
            self.check_object_permissions(self.request, obj=unit_to_delete)
            unit_to_delete.delete()
            return Response(data={'detail': 'Successfully deleted'}, status=status.HTTP_200_OK)
        except Unit.DoesNotExist:
            return Response(data={'detail': 'Indicated unit does not exist'}, status=status.HTTP_404_NOT_FOUND)


class UnitRetrieveUpdateDestroyAPIView(RetrieveUpdateAPIView):
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
        except (AttendedCourse.DoesNotExist, TypeError):
            return None

    def get_queryset(self):
        try:
            return AttendedCourse.objects.filter(user=self.request.user)
        except TypeError:
            return None

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

    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Method \PUT\ is not allowed'}, status=status.HTTP_403_FORBIDDEN)

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


class AssignmentListCreateAPIView(ListCreateAPIView, DestroyAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [AssignmentPermission]

    def get_queryset(self):
        try:
            return Assignment.objects.select_related('unit__course').filter(unit__pk=self.kwargs.get('unit_pk'))
        except (KeyError, AttributeError):
            return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            unit = Unit.objects.select_related('course', 'course__owner').get(pk=self.kwargs.get('unit_pk'))
        except Unit.DoesNotExist:
            return Response(data={'detail': 'Indicated unit does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if request.user != unit.course.owner:
            return Response({'detail': 'You do not have permission to create assignment for this course'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data, context={'unit': unit})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            assignment_to_delete = Assignment.objects.get(pk=self.request.data.get('assignment_id'))
            self.check_object_permissions(self.request, obj=assignment_to_delete)
            assignment_to_delete.delete()
            return Response(data={'detail': 'Successfully deleted'}, status=status.HTTP_200_OK)
        except (Assignment.DoesNotExist, KeyError, AttributeError):
            return Response(data={'detail': 'Indicated unit does not exist'}, status=status.HTTP_404_NOT_FOUND)


class AssignmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [AssignmentPermission]

    def get_object(self):
        try:
            assignment = Assignment.objects.get(pk=self.kwargs.get('assignment_pk'), unit__pk=self.kwargs.get('unit_pk'))
            self.check_object_permissions(self.request, assignment)
            return assignment
        except Assignment.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        assignment = self.get_object()
        if not assignment:
            return Response(data={'detail': 'Assignment does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance=assignment)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        assignment = self.get_object()
        self.check_object_permissions(request, assignment)
        if not assignment:
            return Response(data={'detail': 'Assignment does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data, instance=assignment)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        assignment = self.get_object()
        if not assignment:
            return Response(data={'detail': 'Assignment does not exist'}, status=status.HTTP_404_NOT_FOUND)

        assignment.delete()
        return Response({'detail': 'Successfully deleted'}, status=status.HTTP_200_OK)
