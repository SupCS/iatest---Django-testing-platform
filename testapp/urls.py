from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="main"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.ProfileEditView.as_view(), name="profile_edit"),
    path("addsubject/", views.SubjectAddingView.as_view(), name="add_subject"),
    path("c/<code>/", views.CourseView.as_view(), name="course"),
    path("new_course/", views.NewCourseView.as_view(), name="add_course"),
    path("join_course/", views.JoinCourseView.as_view(), name="join_course"),
    path("c/<code>/new_test/", views.NewTestView.as_view(), name="add_test"),
    path("c/<code>/t/<id>/", views.TestView.as_view(), name="test"),
    path("c/<code>/t/<id>/overview/", views.testoverview, name="t_overview"),
    path("c/<code>/overview/", views.courseoverview, name="c_overview"),
    path("submition/<int:id>/", views.answersoveriew, name="answers_overview"),
    path("c/<code>/delete/", views.delete_course, name="delete_course"),
    path("c/<code>/<id>/delete/", views.delete_test, name="delete_test"),
]
