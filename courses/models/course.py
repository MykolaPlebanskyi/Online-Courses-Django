from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=50, null=False)
    slug = models.CharField(max_length=50, null=False, unique=True)
    description = models.CharField(max_length=500, null=True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False, default=0)
    active = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="files/thumbnail")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Курси'
        verbose_name_plural = 'Курси'



class CourseProperty(models.Model):
    description = models.CharField(max_length=100, null=False)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Learning(CourseProperty):
    pass

class Test(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='test', null=True)
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return f"Тест для {self.course.name}:"
    
    class Meta:
        verbose_name = 'Тести'
        verbose_name_plural = 'Тести'

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=200, null=False)
    
    def __str__(self):
        return f"{self.test}, питання: {self.text}"
    
    class Meta:
        verbose_name = 'Питання'
        verbose_name_plural = 'Питання'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, null=False)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Відповідь до {self.question.text}: {self.text}"
