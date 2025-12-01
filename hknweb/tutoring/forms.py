from django import forms

from dal import autocomplete

from hknweb.coursesemester.models import Course
from hknweb.studentservices.models import CourseDescription
from hknweb.tutoring.views.autocomplete import get_tutors


class CourseFilterForm(forms.Form):
    course = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=autocomplete.ModelSelect2Multiple(
            url="tutoring:autocomplete_course",
            attrs={"onchange": "selector_decorator()"},
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.all()


class TutorFilterForm(forms.Form):
    tutor = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=autocomplete.ModelSelect2Multiple(
            url="tutoring:autocomplete_tutor",
            attrs={"onchange": "selector_decorator()"},
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tutor"].queryset = get_tutors()


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = CourseDescription
        fields = ["title", "slug"]


class TutoringSignUpForm(forms.Form):
    """Form for officers to indicate tutoring availability"""

    # Building preferences
    cory_preference = forms.BooleanField(
        required=False, initial=True, label="Cory Hall"
    )
    soda_preference = forms.BooleanField(
        required=False, initial=True, label="Soda Hall"
    )

    # Adjacent slots preference
    adjacent_slots = forms.ChoiceField(
        choices=[
            ("-1", "Don't care"),
            ("0", "Prefer not adjacent"),
            ("1", "Prefer adjacent"),
        ],
        widget=forms.Select,
        initial="-1",
        label="Adjacent Slots Preference",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create fields for each time slot
        # Format: slot_<weekday>_<hour> (e.g., slot_0_12 for Monday 12 PM)
        weekdays = range(5)  # Mon-Fri (0-4)
        hours = [12, 13, 14, 15, 16]  # 12 PM - 4 PM

        for weekday in weekdays:
            for hour in hours:
                field_name = f"slot_{weekday}_{hour}"
                self.fields[field_name] = forms.ChoiceField(
                    choices=[
                        ("0", "Cannot make it"),
                        ("1", "Less preferred"),
                        ("2", "Can make it"),
                        ("3", "Preferred"),
                    ],
                    initial="0",
                    required=False,
                    widget=forms.RadioSelect(attrs={"class": "preference-radio-input"}),
                )