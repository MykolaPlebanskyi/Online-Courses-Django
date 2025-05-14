from courses.models import Course, UserCourse, CouponCode
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal, ROUND_DOWN


@login_required(login_url='/login')
def checkout(request, slug):
    course = get_object_or_404(Course, slug=slug)
    profile = request.user.profile
    couponcode = request.GET.get('couponcode')
    coupon = None
    coupon_code_message = None
    order = None
    error = None

    try:
        user_course = UserCourse.objects.get(profile=profile, course=course)
        error = "You are Already Enrolled in this Course"
    except UserCourse.DoesNotExist:
        pass

    amount = None
    if error is None:
        amount = int((course.price - (course.price * course.discount * 0.01)) * 100)

    if amount == 0:
        UserCourse.objects.create(profile=profile, course=course)
        return redirect('my-courses')

    if couponcode:
        try:
            coupon = CouponCode.objects.get(course=course, code=couponcode)
            UserCourse.objects.create(profile=profile, course=course)
            return redirect('my-courses')
        except CouponCode.DoesNotExist:
            coupon_code_message = 'Такого купона не існує'

    context = {
        "course": course,
        "order": order,
        "user": profile.user,
        "error": error,
        "coupon": coupon,
        "coupon_code_message": coupon_code_message
    }
    return render(request, "courses/check_out.html", context)



@login_required
@csrf_exempt
def pay_with_balance(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    profile = request.user.profile
    user = request.user

    course_price = Decimal(course.price) * (Decimal(1) - Decimal(course.discount) / Decimal(100))
    course_price = course_price.quantize(Decimal('1'), rounding=ROUND_DOWN)

    if profile.balance >= course_price:
        profile.balance -= course_price
        profile.save()

        userCourse = UserCourse(profile=profile, course=course)
        userCourse.save()

        return redirect('my-courses')
    else:
        return render(request, "courses/check_out.html", {
            "course": course,
            "coupon_code_message": "Недостатньо коштів!"
        })


