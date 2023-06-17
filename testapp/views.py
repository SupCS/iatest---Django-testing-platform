import json
from datetime import datetime, timedelta
from math import ceil  # Для округлення вгору

from django.contrib.auth.decorators import login_required
from django.http import (  # Для повернення простого респонзу та помилки 404
    HttpResponse,
    HttpResponseNotFound,
)
from django.shortcuts import redirect, render
from django.utils import timezone  # Пакет інструментів для роботи з нашою таймзоною
from django.views import View

# Функція для генерації коду курсу, отримання правильної відповіді на питання, розбивання пачки тестів на сторінки
from testapp.funcs import create_random_chars, cut_by_page, get_correct

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


@login_required(login_url="login")
def profile_view(request):
    current_teacher = Teacher.objects.all().filter(
        user_id=request.user
    )  # Пробуємо знайти об'єкт вчителя з user_id == request.user
    if current_teacher:  # Якщо знайшли
        subjects = current_teacher[
            0
        ].subjects.all()  # Отримуємо всі предмети, які викладає вчитель
        courses = Course.objects.filter(
            users__in=[request.user]
        )  # Всі курси, які він веде
        course_list = []
        for course in courses:
            desc = course.description
            if len(course.description) > 214:
                desc = course.description[:213] + '...'
            course_list.append({'c':course, 'desc':desc})
        ctx = {"teacher": current_teacher[0], "subjects": subjects, "courses": course_list}
        return render(request, "testapp/teacher_profile.html", ctx)
    else:  # Інакше перед нами студент
        current_student = Student.objects.get(
            user_id=request.user
        )  # Отримуємо відповідний об'єкт
        courses = Course.objects.filter(
            users__in=[request.user]
        )  # Та всі курси, на яких він вчиться
        course_list = []
        for course in courses:
            desc = course.description
            if len(course.description) > 214:
                desc = course.description[:213] + '...'
            course_list.append({'c':course, 'desc':desc})
        ctx = {"student": current_student, "courses": course_list}
        return render(request, "testapp/student_profile.html", ctx)


class ProfileEditView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(
                "login"
            )  # Якщо юзер не ввійшов в акаунт - відправляємо логінитися
        if request.user.status == "T":
            # Якщо вчитель, отримуємо перелік предметів (subjects) та обраних за замовчуванням предметів (sel_subjects)
            current_teacher = Teacher.objects.get(user_id=request.user)
            subjects = Subject.objects.all()
            sel_subjects = Subject.objects.filter(teachers__in=[current_teacher])
            ctx = {
                "teacher": current_teacher,
                "subjects": subjects,
                "sel_subjects": sel_subjects,
            }
            return render(request, "testapp/teacher_edit.html", ctx)
        else:
            # Студенту - пакуємо перелік груп
            current_student = Student.objects.get(user_id=request.user)
            groups = Group.objects.all()
            ctx = {"student": current_student, "groups": groups}
            return render(request, "testapp/student_edit.html", ctx)

    def post(self, request):
        # Збираємо аргументи з посту та переписуємо всі поля об'єкту вчителя чи студента
        # При початковому рендерингу сторінки в методі get(), ми заповнюємо поля дефолтними значеннями,
        # тож навіть якщо користувач їх не змінював - дані збережуться коректно
        if request.user.status == "T":
            args = request.POST
            name = args.get("full_name")
            contacts = args.get("contacts")
            subjects = args.getlist("subjects")
            teacher = Teacher.objects.get(user_id=request.user)
            teacher.subjects.clear()
            for subject in subjects:
                sub_obj = Subject.objects.get(subject_name=subject)
                teacher.subjects.add(sub_obj)
            teacher.full_name = name
            teacher.contacts = contacts
            teacher.save()
        else:
            args = request.POST
            name = args.get("full_name")
            if args.get("group") == "add":
                try:
                    group = Group.objects.get(group_code=args.get("n_group"))
                except:
                    group = Group(group_code=args.get("n_group"))
                    group.save()
            else:
                group = Group.objects.get(group_code=args.get("group"))
            student = Student.objects.get(user_id=request.user)
            student.full_name = name
            student.group = group
            student.save()
        return redirect("profile")


class NewCourseView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        if (
            request.user.status != "T"
        ):  # Якщо юзер не вчитель - не пускаємо на сторінку створення курсу
            return HttpResponseNotFound()
        return render(request, "testapp/new_course.html")

    def post(self, request):
        if request.user.status != "T":
            return HttpResponseNotFound()
        args = request.POST
        name = args.get("name")
        desc = args.get("description")
        code = None
        while not code:
            code = create_random_chars(10)
            course = Course.objects.filter(code=code).first()
            if course:
                code = None

        new_course = Course(title=name, description=desc, code=code)
        new_course.save()  # Збираємо дані з полів та створюємо новий курс
        new_course.users.add(
            request.user
        )  # Одразу додаємо вчителя, який його створив як нового користувача
        return redirect("course", code=code)


@login_required(login_url="login")
def delete_course(request, code):
    course = Course.objects.get(code=code)  # Отримуємо курс за кодом
    if request.user.status == "T" and request.user in course.users.all().filter(
        status="T"
    ):  # Видаляємо, якщо це робить вчитель цього курсу
        course.delete()
        return redirect("profile")
    return HttpResponseNotFound()


@login_required(login_url="login")
def delete_test(request, code, id):
    course = Course.objects.get(code=code)  # Отримуємо курс за кодом
    test = Test.objects.get(id=id)  # Отримуємо тест за id
    if request.user.status == "T" and request.user in course.users.all().filter(
        status="T"
    ):  # Видаляємо, якщо це робить вчитель цього курсу
        test.delete()
        return redirect("course", code=code)
    return HttpResponseNotFound()


@login_required(login_url="login")
def delete_test(request, code, id):
    course = Course.objects.get(code=code)  # Отримуємо курс за кодом
    test = Test.objects.get(id=id)  # Отримуємо тест за id
    if request.user.status == "T" and request.user in course.users.all().filter(
        status="T"
    ):  # Видаляємо, якщо це робить вчитель цього курсу
        test.delete()
        return redirect("course", code=code)
    return HttpResponseNotFound()


class SubjectAddingView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user.status != "T":
            return HttpResponseNotFound()
        return render(
            request, "testapp/add_subject.html"
        )  # До створення нового предмету допускаємо лише вчителів

    def post(self, request):
        if request.user.status == "T":
            new_sub = request.POST.get("subject")  # Беремо назву предмету з поля
            try:
                created_sub = Subject.objects.get(
                    subject_name=new_sub
                )  # Пробуємо взяти такий об'єкт з бази даних
            except:
                created_sub = Subject(subject_name=new_sub)
                created_sub.save()  # Якщо не виходить - створюємо новий та зберігаємо
            if request.POST.get("add"):
                created_sub.teachers.add(
                    Teacher.objects.get(user_id=request.user)
                )  # Якщо вчитель не прибрав галочку - одразу додаємо до його предметів
        return redirect("profile")


class JoinCourseView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(
                request, "testapp/enter_course.html"
            )  # До курсу допускаємо лише аутентифікованих користувачів
        else:
            return redirect("login")

    def post(self, request):
        args = request.POST
        code = args.get("code")  # Беремо код курсу з поля
        try:
            course = Course.objects.get(code=code)
            course.users.add(request.user)
            return redirect(
                "course", code=code
            )  # Шукаємо його, додаємо туди користувача та перекидаємо на сторінку курсу
        except:
            return HttpResponse(
                "Курс не знайдено"
            )  # Якщо не знаходимо - повідомляємо користувачу


class CourseView(View):
    def get(self, request, code):
        course = Course.objects.get(code=code)
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user not in course.users.all():
            return HttpResponseNotFound()
        try:
            course = Course.objects.get(code=code)  # Отримуємо курс за кодом
        except Course.DoesNotExist:
            return HttpResponseNotFound()
        tusers = course.users.all().filter(
            status="T"
        )  # Отримуємо перелік вчителів (users)
        teachers = []
        for user in tusers:
            tuser = Teacher.objects.get(user_id=user)
            teachers.append(tuser)  # Отримуємо перелік вчителів (teachers)
        tests = Test.objects.filter(course=course)  # Отримуємо перелік тестів
        # Сортуємо тести на активні, заплановані та завершені. Також для студентів збираємо пакет пройдених тестів
        present_tests = tests.filter(
            time_to_publish__lte=timezone.localtime(timezone.now())
        )
        future_tests = tests.filter(
            time_to_publish__gte=timezone.localtime(timezone.now())
        )
        past_tests = present_tests.filter(
            deadline__lte=timezone.localtime(timezone.now())
        )
        present_tests = present_tests.filter(
            deadline__gte=timezone.localtime(timezone.now())
        )
        comp_tests = []
        if request.user.status == "S":
            all_comp = Submition.objects.filter(
                student=Student.objects.get(user_id=request.user)
            )
            for test in present_tests:
                sub = all_comp.filter(test=test)
                if sub:
                    comp_tests.append(test)
        # Рендеримо сторінку
        ctx = {
            "course": course,
            "teachers": teachers,
            "present": present_tests,
            "future": future_tests,
            "past": past_tests,
            "completed": comp_tests,
        }
        return render(request, "testapp/course.html", ctx)


class NewTestView(View):
    def get(self, request, code):
        return render(request, "testapp/newtest.html", {"code": code})

    def post(self, request, code):
        args = request.POST
        print(args)
        t = Test(
            title=args.get("qname"),
            description=args.get("desc"),
            time_to_submit=timedelta(days=0, hours=int(args.get("hours")), minutes=int(args.get("minutes")),
                seconds=int(args.get("seconds")), microseconds=0),
            time_to_publish=args.get("pub_time"),
            max_points=args.get("m_points"),
            course=Course.objects.get(code=code),
            deadline=args.get("deadline"),
        )  # Отримуємо купу даних з полів та створюємо об'єкти тесту
        t.save()
        print(t.time_to_submit)
        for quetion in json.loads(
            request.POST.get("q")
        ):  # Та об'єкти питань та відповідей
            q = Quetion(
                content=quetion.get("text"), points=quetion.get("points"), test=t
            )
            q.save()
            for answer in quetion.get("ans"):
                a = Answer(
                    content=answer.get("text"),
                    is_correct=answer.get("is_correct"),
                    quetion=q,
                )
                a.save()
        return (
            HttpResponse()
        )  # Даємо звичайний респонз, JS все одно нас на курс перекине


class TestView(View):
    def get(self, request, code, id):
        if not request.user.is_authenticated:
            return HttpResponseNotFound()
        course = Course.objects.get(
            code=code
        )  # Нам по суті це не треба, але якщо беремо код, то чого б не знайти курс, лол
        test = Test.objects.get(id=id)  # Знаходимо всі тести курсу
        quetions = Quetion.objects.filter(test=test)  # Знаходимо питання
        out = []
        # Для кожного питання визначаємо тип: радіо чи чекбокс (1 чи декілька відповідей)
        # Засовуємо це все в аутпут
        # В МАЙБУТНЬОМУ: засунути це все у функцію з funcs.py
        for quet in quetions:
            corrects = 0
            answers = list(Answer.objects.filter(quetion=quet))
            for answer in answers:
                if answer.is_correct:
                    corrects += 1
            if corrects > 1:
                type = "check"
            else:
                type = "radio"
            out.append({"quetion": quet, "answers": answers, "type": type})
        time = {
            "minutes" : test.time_to_submit.seconds // 60,
            "secs" : test.time_to_submit.seconds % 60
        }
        print(time)
        ctx = {"test": test, "quetions": out, "time" : time, "course" : course}
        if request.user.status == "S":  # Якщо наш користувач - студент
            if test.time_to_publish >= timezone.localtime(
                timezone.now()
            ) or test.deadline <= timezone.localtime(timezone.now()):
                return (
                    HttpResponseNotFound()
                )  # Якщо тест прострочений чи ще не опублікований - викидаємо 404
            subs = Submition.objects.filter(test=test)
            student = Student.objects.get(
                user_id=request.user
            )  # Знаходимо об'єкт студента
            try:
                submition = subs.get(student=student)
                return HttpResponseNotFound()
            except Submition.DoesNotExist:
                pass
            new_sub = Submition(
                submited=False,
                student=Student.objects.get(user_id=request.user),
                points=0,
                test=test,
            )
            new_sub.save()  # Створюємо нове проходження одразу як користувач зайшов на сторінку. Вийде не завершивши - його проблеми
        return render(request, "testapp/test.html", ctx)

    def post(self, request, code, id):
        course = Course.objects.get(code=code)
        test = Test.objects.get(id=id)
        quetions = Quetion.objects.filter(test=test)
        real_max = 0  # Сума максимальних балів за кожне питання
        points = 0  # Набрані бали
        all_answers = []  # ІД відповідей, для подальшого зберігання в базу
        # Далі іде довга і незрозуміла система підрахунку балів
        # Не бачу сенсу її коментувати, адже вона навряд буде змінюватися
        for quetion in quetions:
            real_max += quetion.points
            answers = list(
                Answer.objects.filter(quetion=quetion)
            )  # Надо загнать под функцию
            corrects = 0  # Функцию добавить в funcs.py
            for answer in answers:  # функция принимает quetion (type == Quetion)
                if answer.is_correct:  # возвращает type == 'check' or type == 'radio'
                    corrects += 1  # После этого переработать метод get()
            if corrects > 1:
                type = "check"
            else:
                type = "radio"
            if type == "radio":
                all_answers.append(request.POST.get(str(quetion.id)))
                if str(get_correct(quetion)) == request.POST.get(str(quetion.id)):
                    points += quetion.points
            elif type == "check":
                answers = Answer.objects.filter(quetion=quetion)
                points_per_answer = quetion.points / len(answers)
                for ans in answers:
                    print(request.POST.get(str(ans.id)))
                    if request.POST.get(str(ans.id)) and ans.is_correct:
                        print('br1')
                        points += points_per_answer
                        all_answers.append(str(ans.id))
                    elif not request.POST.get(str(ans.id)) and not ans.is_correct:
                        print('br2')
                        points += points_per_answer
                    elif not request.POST.get(str(ans.id)) and ans.is_correct:
                        print('br3')
                    else:
                        print('br4')
                        all_answers.append(str(ans.id))

        mark = int(
            test.max_points * (points / real_max)
        )  # Вираховуємо реальну оцінку, за даною шкалою
        subs = Submition.objects.filter(test=test)
        sub = subs.get(student=Student.objects.get(user_id=request.user))
        sub.points = mark
        sub.submited = True
        for (
            answer
        ) in all_answers:  # Зберігаємо у базу питання, на які відповів наш студент
            sub.answers.add(Answer.objects.get(id=int(answer)))
            print(Answer.objects.get(id=int(answer)).content)
        sub.save()  # Зберігаємо відредагований сабмішн
        return redirect("course", code)


@login_required(login_url="login")
def testoverview(request, code, id):
    if request.user.status == "T":
        test = Test.objects.get(id=id)
        submitions = Submition.objects.filter(test=test)
        ctx = {"test": test, "subs": submitions}
        return render(
            request, "testapp/test_overview.html", ctx
        )  # Знаходимо тест, всі проходження та будуємо таблицю в хтмл
    else:
        return HttpResponseNotFound()  # А якщо зайшов студент - виганяємо його


@login_required(login_url="login")
def answersoveriew(request, id):
    if request.user.status == "T":
        sub = Submition.objects.get(id=id)
        student_answers = sub.answers.get_queryset()
        questions = []
        for question in sub.test.quetion_set.get_queryset():
            corrects = 0
            answers = []
            for answer in question.answer_set.get_queryset():
                if answer.is_correct:
                    corrects += 1
                student_choice = answer in student_answers
                answers.append({"answer": answer, "student_choice": student_choice})
            if corrects > 1:
                type = 'check'
            else:
                type = 'radio'
            questions.append({"question": question, "answers": answers, "type": type})
        print(questions)
        ctx = {
            "submition": sub,
            "questions": questions,
        }
        return render(request, "testapp/answers.html", ctx)
    else:
        return HttpResponseNotFound()


@login_required(login_url="login")
def courseoverview(request, code):
    if request.user.status != "T":  # Студентів не пропустимо!
        return HttpResponseNotFound()
    course = Course.objects.get(code=code)
    tests = Test.objects.filter(course=course)
    s_users = course.users.filter(status="S")  # Збираємо кверісет студентів цього курсу
    students = []  # Та будуємо масив відповідних об'єктів моделі студент
    for s_user in s_users:
        student = Student.objects.get(user_id=s_user)
        students.append(student)
    pages = ceil(len(tests) / 5)  # Вираховуємо кількість сторінок
    # Якщо є ГЕТ-аргумент "сторінка" - то використовуємо її, інакше - переходимо на першу
    if request.GET.get("page"):
        page = int(request.GET.get("page"))
    else:
        page = 1
    tests = cut_by_page(
        tests, page
    )  # Вирізаємо шматочок кверісету тестів за нашою сторінкою
    out = []  # Створюємо масив зі словниками для кожного студенту
    # У словниках є об'єкт студента та його оцінки для даних тестів
    for student in students:
        subs = Submition.objects.filter(student=student)
        results = []
        for test in tests:
            try:
                sub = subs.get(test=test)
                sub_id = sub.id
            except Submition.DoesNotExist:
                sub = None
                sub_id = None
            if sub:
                mark = sub.points
            else:
                mark = "N/A"
            results.append({"mark" : mark, "id" : sub_id})
        out.append({"student": student, "results": results})
    ctx = {
        "course": course,
        "tests": tests,
        "students": out,
        "pages": pages,
        "page": page,
    }
    return render(request, "testapp/course_overview.html", ctx)
