from django.db import models


class PlacementQuestion(models.Model):
    text = models.CharField(max_length=200, null=False)

    def __str__(self):
        return f"Питання: {self.text}"

    class Meta:
        verbose_name = 'Питання до тесту'
        verbose_name_plural = 'Питання до тесту'


class PlacementAnswer(models.Model):
    question = models.ForeignKey(PlacementQuestion, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=200, null=False)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Відповідь до {self.question.text}: {self.text}"

    class Meta:
        verbose_name = 'Відповідь'
        verbose_name_plural = 'Відповіді'


class PlacementTest(models.Model):
    LANGUAGES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('cz', 'Czech'),
        ('tu', 'Turkish'),
        ('ch', 'Chinese'),
        ('fr', 'French'),
    ]
    name = models.CharField(max_length=50, null=False, default="Placement Test")
    language = models.CharField(max_length=2, choices=LANGUAGES, null=False, default='en')
    questions = models.ManyToManyField(PlacementQuestion, related_name='tests')

    def __str__(self):
        return f"Тест {self.name} на рівень мови {self.get_language_display()}"

    class Meta:
        verbose_name = 'Тест на рівень'
        verbose_name_plural = 'Тести на рівень'