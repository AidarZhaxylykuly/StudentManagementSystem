from rest_framework import serializers
from .models import Grade
from students.models import Student
from courses.models import Course


class GradeSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Grade
        fields = ['student', 'course', 'grade', 'date', 'teacher']

    def create(self, validated_data):
        return Grade.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.grade = validated_data.get('grade', instance.grade)
        instance.save()
        return instance