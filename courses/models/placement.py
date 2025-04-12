from django.db import models
from courses.models import Course


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
        # Додавай інші мови, якщо потрібно
    ]
    language = models.CharField(max_length=2, choices=LANGUAGES, null=False, default='en')

    name = models.CharField(max_length=50, null=False, default="Placement Test")

    def __str__(self):
        return f"Тест для {self.name} на рівень мови"

    class Meta:
        verbose_name = 'Тест на рівень'
        verbose_name_plural = 'Тест на рівень'


class PlacementQuestion(models.Model):
    test = models.ForeignKey(PlacementTest, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=200, null=False)

    def __str__(self):
        return f"{self.test}, питання: {self.text}"

    class Meta:
        verbose_name = 'Питання до тесту'
        verbose_name_plural = 'Питання до тесту'


class PlacementAnswer(models.Model):
    question = models.ForeignKey(PlacementQuestion, on_delete=models.CASCADE,  related_name='answers')
    text = models.CharField(max_length=200, null=False)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Відповідь до {self.question.text}: {self.text}"
