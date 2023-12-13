from django.db import models
from courses.models import Course
from courses.models import UserCourse
from django.contrib.auth.models import User

class CouponCode(models.Model):
    code = models.CharField(max_length=6)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='coupons')
    
    def __str__(self):
        return f'Код для {self.course} : {self.code}'
    
    class Meta:
        verbose_name = 'Купони'
        verbose_name_plural = 'Купони'
    




    