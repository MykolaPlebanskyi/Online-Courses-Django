from django.shortcuts import render , redirect
from courses.models import Course , Video , UserCourse, CouponCode
from django.shortcuts import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from online_courses.settings import *
from time import time


@login_required(login_url='/login')
def checkout(request , slug):
    course = Course.objects.get(slug  = slug)
    user = request.user
    couponcode = request.GET.get('couponcode')
    coupon = None
    coupon_code_message = None
    order = None
    error = None
    try:
        user_course = UserCourse.objects.get(user = user  , course = course)
        error = "You are Already Enrolled in this Course"
    except:
        pass
    amount=None
    if error is None : 
        amount =  int((course.price - ( course.price * course.discount * 0.01 )) * 100)
    
    if amount==0:
        userCourse = UserCourse(user = user , course = course)
        userCourse.save()
        return redirect('my-courses')   


    if couponcode:
        try:
            coupon = CouponCode.objects.get(course=course, code = couponcode)
            userCourse = UserCourse(user = user , course = course)
            userCourse.save()
            return redirect('my-courses')   
        except:
            coupon_code_message = 'Такого купона не існує'
            # print('Coupon code invalid')
    
    
    
    
    context = {
        "course" : course , 
        "order" : order, 
        "user" : user , 
        "error" : error,
        "coupon": coupon,
        "coupon_code_message": coupon_code_message
    }
    return  render(request , template_name="courses/check_out.html" , context=context )    

        
 
