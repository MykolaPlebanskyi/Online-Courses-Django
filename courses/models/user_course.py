from django.db import models
from courses.models import Profile
from courses.models import Course


class UserCourse(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Активний'),
        ('Complete', 'Завершений'),
    )

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f'{self.profile.user.username} - {self.course.name}'

    class Meta:
        verbose_name = 'Курси користувачів'
        verbose_name_plural = 'Курси користувачів'
