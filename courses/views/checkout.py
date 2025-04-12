from django.shortcuts import render, redirect
from courses.models import Course, Video, UserCourse, CouponCode, Profile
from django.shortcuts import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from online_courses.settings import *
from time import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal, ROUND_DOWN


@login_required(login_url='/login')
def checkout(request, slug):
    course = Course.objects.get(slug=slug)
    user = request.user
    couponcode = request.GET.get('couponcode')
    coupon = None
    coupon_code_message = None
    order = None
    error = None
    try:
        user_course = UserCourse.objects.get(user=user, course=course)
        error = "You are Already Enrolled in this Course"
    except:
        pass
    amount = None
    if error is None:
        amount = int((course.price - (course.price * course.discount * 0.01)) * 100)

    if amount == 0:
        userCourse = UserCourse(user=user, course=course)
        userCourse.save()
        return redirect('my-courses')

    if couponcode:
        try:
            coupon = CouponCode.objects.get(course=course, code=couponcode)
            userCourse = UserCourse(user=user, course=course)
            userCourse.save()
            return redirect('my-courses')
        except:
            coupon_code_message = 'Такого купона не існує'
            # print('Coupon code invalid')

    context = {
        "course": course,
        "order": order,
        "user": user,
        "error": error,
        "coupon": coupon,
        "coupon_code_message": coupon_code_message
    }
    return render(request, template_name="courses/check_out.html", context=context)


@login_required
@csrf_exempt
def pay_with_balance(request, course_id):
    course = get_object_or_404(Course, id=course_id)  # Отримуємо курс за id
    profile = request.user.profile  # Отримуємо профіль користувача
    user = request.user  # Отримуємо поточного користувача

    # Обчислюємо ціну курсу з урахуванням знижки
    course_price = Decimal(course.price) * (Decimal(1) - Decimal(course.discount) / Decimal(100))
    course_price = course_price.quantize(Decimal('1'), rounding=ROUND_DOWN)

    # Перевіряємо, чи є достатньо коштів на балансі
    if profile.balance >= course_price:
        # Якщо є достатньо коштів, зменшуємо баланс користувача і зберігаємо зміни
        profile.balance -= course_price
        profile.save()

        # Створюємо запис в UserCourse для відслідковування курсу
        userCourse = UserCourse(user=user, course=course)
        userCourse.save()

        # Перенаправляємо на сторінку моїх курсів
        return redirect('my-courses')
    else:
        # Якщо коштів недостатньо, повертаємо помилку і показуємо повідомлення
        return render(request, "courses/check_out.html", {
            "course": course,
            "coupon_code_message": "Недостатньо коштів!"  # Передаємо повідомлення в контекст
        })


