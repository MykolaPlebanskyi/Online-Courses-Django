from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Settings(models.Model):
    coin_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1)  # Курс обміну монет

    def __str__(self):
        return self.coin_rate

    class Meta:
        verbose_name = 'Курс обміну монет'
        verbose_name_plural = 'Курс обміну монет'


class Profile(models.Model):
    ROLE_CHOICES = (
        ('Студент', 'Студент'),
        ('Викладач', 'Викладач'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='files/avatars/', default='files/avatars/default.png')
    registration_date = models.DateTimeField(default=timezone.now)
    start_test = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coins = models.IntegerField(default=200)
    courses = models.ManyToManyField('Course', through='UserCourse', related_name='students')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Студент')

    def exchange_coins(self, coins_to_exchange):
        """
        Обмін монет на гривні з урахуванням динамічного курсу.
        """
        settings = Settings.objects.first()
        if not settings or coins_to_exchange <= 0 or coins_to_exchange > self.coins:
            return False

        coin_rate = settings.coin_rate
        self.balance += coins_to_exchange / coin_rate
        self.coins -= coins_to_exchange
        self.save()
        return True

    def pay_for_course(self, course):
        """Оплата курсу через баланс"""
        sell_price = course.price * (1 - course.discount / 100)

        if self.balance >= sell_price:
            self.balance -= sell_price
            self.save()
            return True
        return False

    def __str__(self):
        return f'У користувача {self.user}, баланс: {self.balance}, монет: {self.coins}'


    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Баланс'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance, role='Студент')