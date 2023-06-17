from django.contrib import admin

from .models import (
    Answer,
    Course,
    Group,
    Quetion,
    Student,
    Subject,
    Submition,
    Teacher,
    Test,
)


class TestAdmin(admin.ModelAdmin):
    readonly_fields = ("time_to_publish",)


admin.site.register(Test, TestAdmin)

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(Course)
admin.site.register(Quetion)
admin.site.register(Answer)
admin.site.register(Submition)
