from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text
from django.utils import timezone
from .models import *
from accounts.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name',
        )


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    """
    参考:
    https://stackoverflow.com/questions/28009829/creating-and-saving-foreign-key-objects-using-a-slugrelatedfield
    """
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all(), required=True)
    # user = UserSerializer(many=False, required=True)
    tag = CreatableSlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Note
        fields = (
            'id',
            'title',
            'content',
            'locate',
            'date',
            'start',
            'end',
            'elapsed_time',
            'user',
            'tag',
            'text_type',
            'has_metadata'
        )


class CommentSerializer(serializers.ModelSerializer):
    posted_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'name',
            'content',
            'note',
            'user',
            'anonymous',
            'posted_date',
        )

    def create(self, validated_data):
        return Comment.objects.create(
            name=validated_data['name'],
            content=validated_data['content'],
            note=validated_data['note'],
            anonymous=validated_data['anonymous'],
            posted_date=timezone.now()
        )

