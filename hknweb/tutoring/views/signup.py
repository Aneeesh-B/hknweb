from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from hknweb.tutoring.models import TutoringAvailability
from hknweb.tutoring.forms import TutoringSignUpForm


@login_required
def tutoring_signup(request):
    """View for officers to sign up for tutoring slots"""

    if request.method == "POST":
        form = TutoringSignUpForm(request.POST)
        if form.is_valid():
            # Delete existing preferences for this user
            TutoringAvailability.objects.filter(user=request.user).delete()

            # Save new preferences
            weekdays = range(5)  # Mon-Fri (0-4)
            hours = [12, 13, 14, 15, 16]

            adjacent_pref = int(form.cleaned_data["adjacent_slots"])

            for weekday in weekdays:
                for hour in hours:
                    field_name = f"slot_{weekday}_{hour}"
                    preference_level = int(form.cleaned_data.get(field_name, 0))

                    TutoringAvailability.objects.create(
                        user=request.user,
                        semester=None,
                        weekday=weekday,
                        hour=hour,
                        preference_level=preference_level,
                        cory_preference=form.cleaned_data["cory_preference"],
                        soda_preference=form.cleaned_data["soda_preference"],
                        adjacent_slots_preference=adjacent_pref,
                    )

            return redirect("tutoring:signup_success")
    else:
        # Pre-populate form with existing data
        existing_prefs = TutoringAvailability.objects.filter(user=request.user)

        initial_data = {}
        if existing_prefs.exists():
            first_pref = existing_prefs.first()
            initial_data["cory_preference"] = first_pref.cory_preference
            initial_data["soda_preference"] = first_pref.soda_preference
            initial_data["adjacent_slots"] = str(first_pref.adjacent_slots_preference)

            for pref in existing_prefs:
                field_name = f"slot_{pref.weekday}_{pref.hour}"
                initial_data[field_name] = str(pref.preference_level)

        form = TutoringSignUpForm(initial=initial_data)

    context = {"form": form}

    return render(request, "tutoring/signup.html", context)


@login_required
def signup_success(request):
    """Success page after submitting tutoring availability"""
    return render(request, "tutoring/signup_success.html")


@staff_member_required
def get_availability_data(request):
    """API endpoint to get all tutoring availability for scheduling"""

    availabilities = TutoringAvailability.objects.all().select_related("user")

    data = []
    for avail in availabilities:
        data.append(
            {
                "user_id": avail.user.id,
                "user_name": avail.user.get_full_name(),
                "weekday": avail.weekday,
                "hour": avail.hour,
                "preference_level": avail.preference_level,
                "cory_preference": avail.cory_preference,
                "soda_preference": avail.soda_preference,
                "adjacent_slots_preference": avail.adjacent_slots_preference,
            }
        )

    return JsonResponse({"availabilities": data})

