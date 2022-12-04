from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField
from rest_framework.exceptions import ValidationError

from course.models import *


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')


class CourseSerializer(ModelSerializer):
    units = SerializerMethodField(method_name='get_units')
    evaluators = SerializerMethodField(method_name='get_evaluators')
    owner = SerializerMethodField()
    managers = SerializerMethodField()
    editors = SerializerMethodField()

    def get_owner(self, obj):
        return UserSerializer(obj.owner).data


    def get_units(self, obj):
        units = obj.unit_set.all()
        return UnitSerializer(units, many=True).data

    def get_evaluators(self, obj):
        evaluators = obj.evaluators.all()
        return UserSerializer(evaluators, many=True).data

    def get_managers(self, obj):
        managers = obj.managers.all()
        return UserSerializer(managers, many=True).data

    def get_editors(self, obj):
        editors = obj.editors.all()
        return UserSerializer(editors, many=True).data

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        course = Course.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            logo=validated_data['logo'],
            banner=validated_data['banner'],
            owner=validated_data['owner'],
            category=validated_data['category'],
        )
        course.evaluators.set(validated_data['evaluators'])
        course.editors.set(validated_data['editors'])
        course.managers.set(validated_data['managers'])

        return {'title': course.title, 'description': course.description, 'banner': course.banner.url}


class CategorySerializer(ModelSerializer):
    course_set = SerializerMethodField()

    def get_course_set(self, obj):
        courses = obj.course_set.all()
        return CourseSerializer(courses, many=True).data

    class Meta:
        model = Category
        fields = ('course_set', 'title', 'created_at', 'updated_at')


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class LectureSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'


class AttendedCourseSerializer(ModelSerializer):
    user = SerializerMethodField(required=False)
    course = SerializerMethodField()

    def get_course(self, obj):
        return CourseSerializer(obj.course).data

    def get_user(self, obj):
        print(f"obj in gt user {obj}")
        print(self.context)
        return UserSerializer(obj.user).data

    class Meta:
        model = AttendedCourse
        fields = '__all__'

    def create(self, validated_data):
        courses = AttendedCourse.objects.all()
        for course in courses:
            if course.course.id == validated_data['course'].id and course.user == self.context.get('user'):
                raise ValidationError({'user': 'You already attended this course'}, 400)

        attended_course = AttendedCourse.objects.create(
            user=self.context.get('user'),
            course=validated_data['course'],
        )
        return attended_course


class ReviewSerializer(ModelSerializer):
    user = SerializerMethodField(required=False)

    class Meta:
        model = Review
        fields = ('id', 'user', 'feedback_message', 'rating', 'created_at',)

    def get_user(self, obj):
        if obj.user:
            user = User.objects.get(pk=obj.user.pk)
            return {'id': user.pk,
                    'first_name': user.first_name,
                    'last_name': user.last_name}
        return None

    def create(self, validated_data):
        review = Review.objects.create(
            user=self.context.get('user'),
            course=self.context.get('course'),
            feedback_message=validated_data['feedback_message'],
            rating=validated_data['rating']
        )

        return review


class AssignmentSerializer(ModelSerializer):

    class Meta:
        model = Assignment
        fields = '__all__'
