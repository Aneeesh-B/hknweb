from typing import Union

from datetime import time

from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.auth.models import User

from hknweb.coursesemester.models import Semester


class Room(models.Model):
    name = models.CharField(max_length=25, default="")
    color = models.CharField(max_length=25, default="DarkGray")

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class TutoringLogistics(models.Model):
    class Meta:
        verbose_name_plural = "TutoringLogistics"

    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, null=True, default=None
    )
    one_hour_tutors = models.ManyToManyField(
        User, blank=True, related_name="one_hour_tutoring"
    )
    two_hour_tutors = models.ManyToManyField(
        User, blank=True, related_name="two_hour_tutoring"
    )

    def __str__(self) -> str:  # pragma: no cover
        return str(self.semester)

    @staticmethod
    def get_most_recent() -> "Union[None, TutoringLogistics]":
        logistics: TutoringLogistics = TutoringLogistics.objects.order_by(
            "-semester__year", "semester__semester"
        ).first()

        return logistics


class Slot(models.Model):
    logistics = models.ForeignKey(
        TutoringLogistics, on_delete=models.CASCADE, null=True, default=None
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, default=None)
    num_tutors = models.IntegerField(default=0)
    tutors = models.ManyToManyField(User, blank=True, related_name="tutoring_slots")

    WEEKDAY_STRS = "Mon Tue Wed Thu Fri Sat Sun".split()
    WEEKDAY_CHOICES = list(zip(range(len(WEEKDAY_STRS)), WEEKDAY_STRS))
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, default=0)
    time = models.TimeField(default=time.min)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.logistics} {self.room}"

    def tutor_names(self) -> str:
        tutors = self.tutors.annotate(
            full_name=Concat("first_name", Value(" "), "last_name")
        ).values_list("full_name", flat=True)
        return ", ".join(tutors)


class TutoringAvailability(models.Model):
    """Stores individual tutor's time slot preferences and building preferences"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tutoring_availability"
    )
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, null=True, blank=True
    )

    # Time slot preference (0-3 representing preference levels)
    # 0 = cannot make it (red), 1 = less preferred (yellow),
    # 2 = can make it (blue), 3 = preferred (green)
    weekday = models.IntegerField(choices=Slot.WEEKDAY_CHOICES)
    hour = models.IntegerField(
        choices=[
            (12, "12 PM"),
            (13, "1 PM"),
            (14, "2 PM"),
            (15, "3 PM"),
            (16, "4 PM"),
        ]
    )
    preference_level = models.IntegerField(
        default=0,
        choices=[
            (0, "Cannot make it"),
            (1, "Less preferred but can make it"),
            (2, "Can make it"),
            (3, "Preferred"),
        ],
    )

    # Building preferences
    cory_preference = models.BooleanField(default=True)
    soda_preference = models.BooleanField(default=True)

    # Adjacent slots preference (from old system)
    adjacent_slots_preference = models.IntegerField(
        default=-1,
        choices=[
            (-1, "Don't care"),
            (0, "Prefer not adjacent"),
            (1, "Prefer adjacent"),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "weekday", "hour"]
        ordering = ["weekday", "hour"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user.get_full_name()} - {self.get_weekday_display()} {self.get_hour_display()}"