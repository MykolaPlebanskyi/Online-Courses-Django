from django.db import models


class Course(models.Model):
    LEVELS = [
        ('a1', 'A1'),
        ('a2', 'A2'),
        ('b1', 'B1'),
        ('b2', 'B2'),
        ('c1', 'C1'),
        ('c2', 'C2'),
    ]

    LANGUAGES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('cz', 'Czech'),
        ('tu', 'Turkish'),
        ('ch', 'Chinese'),
        ('fr', 'French'),
        # Додавай інші мови, якщо потрібно
    ]
    name = models.CharField(max_length=50, null=False)
    slug = models.CharField(max_length=50, null=False, unique=True)
    description = models.CharField(max_length=500, null=True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False, default=0)
    active = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="files/thumbnail")
    level = models.CharField(max_length=50, choices=LEVELS, null=False, default='beginner')
    language = models.CharField(max_length=2, choices=LANGUAGES, null=False, default='en')
    tests = models.ManyToManyField('Test', related_name='courses', blank=True)

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


class Question(models.Model):
    text = models.CharField(max_length=200, null=False)

    def __str__(self):
        return f"Питання: {self.text}"

    class Meta:
        verbose_name = 'Питання'
        verbose_name_plural = 'Питання'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=200, null=False)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Відповідь до {self.question.text}: {self.text}"

    class Meta:
        verbose_name = 'Відповідь'
        verbose_name_plural = 'Відповіді'


class Test(models.Model):
    name = models.CharField(max_length=50, null=False)
    questions = models.ManyToManyField(Question, related_name='tests')

    def __str__(self):
        return f"Тест: {self.name}"

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тести'
