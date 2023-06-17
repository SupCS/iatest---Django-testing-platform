from django.conf import settings
from django.db import models


class Group(models.Model):
    group_code = models.CharField(max_length=5)


class Teacher(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    contacts = models.CharField(max_length=100)
    subjects = models.ManyToManyField("Subject", through="TeachersToSubjects")

    def __str__(self):
        return self.full_name


class Student(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    teachers = models.ManyToManyField("Teacher", through="TeachersToSubjects")

    def __str__(self):
        return self.subject_name


class TeachersToSubjects(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Course(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title


class Test(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    max_points = models.DecimalField(max_digits=10, decimal_places=0)
    time_to_submit = models.DurationField()
    time_to_publish = models.DateTimeField(null=True)
    deadline = models.DateTimeField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Quetion(models.Model):
    content = models.CharField(max_length=150)
    points = models.DecimalField(max_digits=10, decimal_places=2)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Answer(models.Model):
    content = models.CharField(max_length=150)
    is_correct = models.BooleanField()
    quetion = models.ForeignKey(Quetion, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Submition(models.Model):
    submited = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    points = models.DecimalField(max_digits=10, decimal_places=0)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer)

    # def __str__(self):
    #     return f"Submission to test {self.test} by student {self.student}"
