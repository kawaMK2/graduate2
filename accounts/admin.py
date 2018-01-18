from django.contrib import admin
from imagekit.admin import AdminThumbnail
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
from imagekit.cachefiles import ImageCacheFile
from .models import *


class AdminThumbnailSpec(ImageSpec):
	# ユーザー管理画面のサムネイルのサイズはここで変更
	processors = [ResizeToFill(20, 20)]
	format = 'JPEG'
	options = {'quality': 60}


def cached_admin_thumb(instance):
	# 'thumbnail' is the name of the image field on the model
	cached = ImageCacheFile(AdminThumbnailSpec(instance.thumbnail))
	# only generates the first time, subsequent calls use cache
	cached.generate()
	return cached


class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'image', 'get_full_name')
	image = AdminThumbnail(image_field=cached_admin_thumb)
	image.short_description = ''


class GradeAdmin(admin.ModelAdmin):
	list_display = ('name', 'formal_name', 'priority')


class BelongAdmin(admin.ModelAdmin):
	list_display = ('user', 'get_grade_name', 'start', 'end')

	def get_grade_name(self, obj):
		return obj.grade.formal_name

	get_grade_name.short_description = 'Grade'


admin.site.register(User, UserAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Belong, BelongAdmin)
