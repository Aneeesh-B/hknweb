from django.urls import path

from . import views

app_name = "tutoring"
urlpatterns = [
    path("", views.index, name="index"),
    path("api/slots", views.slots, name="slots"),
    path(
        "autocomplete/course",
        views.course_autocomplete,
        name="autocomplete_course",
    ),
    path(
        "autocomplete/tutor",
        views.tutor_autocomplete,
        name="autocomplete_tutor",
    ),
    path("portal", views.tutoringportal, name="tutoring_portal"),
    path("courses", views.courses, name="courses"),
    path("signup", views.tutoring_signup, name="signup"),
    path("signup/success", views.signup_success, name="signup_success"),
    path("api/availability", views.get_availability_data, name="availability_data"),
]
