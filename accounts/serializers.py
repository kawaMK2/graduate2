from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from django.utils import timezone

from .models import *


class GradeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Grade
		fields = (
			'id',
			'name',
			'formal_name',
			'priority'
		)


class BelongUserSerializer(serializers.ModelSerializer):
	thumbnail = serializers.ImageField(required=False)

	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'thumbnail'
		)


class BelongSerializer(serializers.ModelSerializer):
	user = BelongUserSerializer()
	grade = GradeSerializer()

	class Meta:
		model = Belong
		fields = (
			'user',
			'grade',
			'start',
			'end'
		)


class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=False)
	# belongs = serializers.PrimaryKeyRelatedField(many=True, queryset=Belong)
	belongs = GradeSerializer(many=True)
	thumbnail = serializers.ImageField(required=False)

	class Meta:
		model = User
		fields = (
			'id',
			'username',
			'first_name',
			'last_name',
			'email',
			'belongs',
			'thumbnail',
			'password'
		)

	def create(self, validated_data):
		user = User(
			username=validated_data['username'],
			email=validated_data['email'],
			is_active=True,
			last_login=timezone.now(),
			date_joined=timezone.now()
		)
		user.set_password(validated_data['password'])
		user.save()
		return user

	def update(self, instance, validated_data):
		# type: (object, object) -> object
		if 'password' in validated_data:
			instance.set_password(validated_data['password'])
		else:
			instance = super(UserSerializer, self).update(instance, validated_data)
		instance.save()
		return instance
