from django.contrib import admin
from .models import *


admin.site.register(Notice)


class Video_TabularInline(admin.TabularInline):
    model = Video

class CourseAdmin(admin.ModelAdmin):
    inlines = [Video_TabularInline]
    list_display = ('title','description')

class CourseAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'category', 'access_granted')
    list_filter = ('user', 'course')



admin.site.register(Categories)

admin.site.register(Author)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(CourseAccess, CourseAccessAdmin)

