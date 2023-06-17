from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View

from testapp.models import Group, Student, Teacher

from .forms import UserCreationForm


class RegisterView(View):

    template_name = "registration/registration.html"

    def get(self, request):
        ctx = {"form": UserCreationForm()}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            status = form.cleaned_data.get("status")
            user = authenticate(username=username, password=password)
            login(request, user)
            if status == "T":
                teacher = Teacher(
                    user_id=user, full_name="Ваше ім'я", contacts="Ваші контакти."
                )
                teacher.save()
            else:
                empty_group = Group.objects.get(group_code="Немає")
                student = Student(
                    user_id=user, full_name="Ваше ім'я", group=empty_group
                )
                student.save()
            return redirect("profile_edit")

        ctx = {"form": form}
        return render(request, self.template_name, ctx)
