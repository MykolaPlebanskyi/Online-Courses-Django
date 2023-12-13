from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Profile
from courses.forms import AvatarForm

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
