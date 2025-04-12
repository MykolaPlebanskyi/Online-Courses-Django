from django.shortcuts import render, redirect
from courses.models import Profile, Settings
from courses.forms import AvatarForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json


@login_required
def user_profile(request):
    user = request.user

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Перенаправлення на сторінку профілю після збереження аватара
    else:
        form = AvatarForm(instance=profile)

    return render(request, 'courses/user_profile.html', {'profile': profile, 'form': form})


@login_required
def exchange_coins(request):
    if request.method == "POST":
        user_profile = request.user.profile
        data = json.loads(request.body)  # Отримуємо JSON-запит
        coins_to_exchange = int(data.get("coins", 0))  # Отримуємо введену кількість монет

        settings = Settings.objects.first()  # Отримуємо актуальний курс
        if not settings:
            return JsonResponse({"success": False, "message": "Курс обміну не налаштований"})

        exchange_rate = settings.coin_rate  # Динамічний курс з БД

        if coins_to_exchange <= 0 or coins_to_exchange > user_profile.coins:
            return JsonResponse({"success": False, "message": "Некоректна кількість монет"})

        # Виконуємо обмін
        user_profile.coins -= coins_to_exchange
        user_profile.balance += coins_to_exchange * exchange_rate
        user_profile.save()

        return JsonResponse({
            "success": True,
            "new_coins": user_profile.coins,
            "new_balance": user_profile.balance
        })

    return JsonResponse({"success": False, "message": "Неправильний запит"})

