from django.contrib import admin

from hknweb.tutoring.models import Room, TutoringLogistics, Slot, TutoringAvailability


@admin.register(TutoringLogistics)
class TutoringLogisticsAdmin(admin.ModelAdmin):
    autocomplete_fields = ("one_hour_tutors", "two_hour_tutors")


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    autocomplete_fields = ("tutors",)


@admin.register(TutoringAvailability)
class TutoringAvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "semester",
        "weekday",
        "hour",
        "preference_level",
        "cory_preference",
        "soda_preference",
    )
    list_filter = (
        "semester",
        "weekday",
        "preference_level",
        "cory_preference",
        "soda_preference",
    )
    search_fields = ("user__first_name", "user__last_name", "user__username")
    autocomplete_fields = ("user",)


admin.site.register(Room)
